"""
Bing Image Search API client
"""

import time
import requests
from typing import Dict, Any, Optional, List, Tuple
from requests.exceptions import RequestException

from image_harvester.utils.logging import get_logger
from image_harvester.utils.config import (
    BING_SEARCH_API_KEY, 
    BING_SEARCH_ENDPOINT,
    DEFAULT_REQUEST_DELAY,
    MAX_RETRY_ATTEMPTS
)
from image_harvester.api.models import SearchResult, ImageMetadata

logger = get_logger(__name__)

class BingImageSearchClient:
    """Client for the Bing Image Search API"""
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        endpoint: Optional[str] = None,
        request_delay: float = DEFAULT_REQUEST_DELAY,
        max_retries: int = MAX_RETRY_ATTEMPTS
    ):
        """
        Initialize the Bing Image Search client
        
        Args:
            api_key: The Bing Search API key (default: from config)
            endpoint: The Bing Search API endpoint (default: from config)
            request_delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts
        """
        self.api_key = api_key or BING_SEARCH_API_KEY
        self.endpoint = endpoint or BING_SEARCH_ENDPOINT
        self.request_delay = request_delay
        self.max_retries = max_retries
        
        # Remember the last request time to enforce rate limiting
        self.last_request_time = 0
        
        if not self.api_key:
            logger.error("No API key provided. Set BING_SEARCH_API_KEY in .env file.")
            raise ValueError("No API key provided")
        
        if not self.endpoint:
            logger.error("No API endpoint provided.")
            raise ValueError("No API endpoint provided")
    
    def search(
        self, 
        query: str, 
        count: int = 50, 
        offset: int = 0,
        market: str = 'en-US',
        safe_search: str = 'Moderate',
        image_type: Optional[str] = None,
        filter: Optional[str] = None,
        **kwargs
    ) -> SearchResult:
        """
        Search for images using the Bing Image Search API
        
        Args:
            query: The search query
            count: Number of results to return (default: 50, max: 150)
            offset: Offset for pagination
            market: Market code (default: en-US)
            safe_search: SafeSearch filter (Off, Moderate, Strict)
            image_type: Type of image (AnimatedGif, Clipart, Line, Photo, etc.)
            filter: OData filter (e.g., color)
            **kwargs: Additional query parameters
            
        Returns:
            SearchResult: The search results
            
        Raises:
            RequestException: If the request fails
        """
        # Enforce rate limiting
        self._enforce_rate_limit()
        
        # Build request parameters
        params = {
            'q': query,
            'count': min(count, 150),  # Maximum allowed by Bing
            'offset': offset,
            'mkt': market,
            'safeSearch': safe_search
        }
        
        # Add optional parameters
        if image_type:
            params['imageType'] = image_type
            
        if filter:
            params['$filter'] = filter
            
        # Add any additional parameters
        params.update(kwargs)
        
        # Build headers
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Accept': 'application/json'
        }
        
        # Make the request with retries
        response_data = self._make_request_with_retries(params, headers)
        
        # Parse the response
        search_result = SearchResult.from_response(query, response_data)
        logger.info(f"Found {len(search_result.images)} images for query: '{query}'")
        
        return search_result
    
    def search_all(
        self, 
        query: str, 
        max_images: int = 100,
        **kwargs
    ) -> SearchResult:
        """
        Search for images and automatically handle pagination to get up to max_images
        
        Args:
            query: The search query
            max_images: Maximum number of images to return
            **kwargs: Additional parameters to pass to search()
            
        Returns:
            SearchResult: Combined search results
        """
        all_images = []
        offset = 0
        count_per_request = min(150, max_images)  # Maximum allowed by Bing
        
        while len(all_images) < max_images:
            # Calculate how many more images we need
            remaining = max_images - len(all_images)
            current_count = min(remaining, count_per_request)
            
            # Make the search request
            logger.info(f"Searching for {current_count} images with offset {offset}...")
            result = self.search(query, count=current_count, offset=offset, **kwargs)
            
            # Add the images to our collection
            all_images.extend(result.images)
            
            # Check if we have more results
            if not result.next_offset or not result.images:
                # No more results available
                logger.info(f"No more results available after {len(all_images)} images")
                break
                
            # Update the offset for the next request
            offset = result.next_offset
            
            # Log progress
            logger.info(f"Retrieved {len(all_images)}/{max_images} images...")
        
        # Create a combined result
        combined_result = SearchResult(
            query=query,
            images=all_images[:max_images],  # Ensure we don't exceed max_images
            total_estimated_matches=result.total_estimated_matches
        )
        
        logger.info(f"Retrieved a total of {len(combined_result.images)} images for query: '{query}'")
        return combined_result
    
    def _enforce_rate_limit(self):
        """
        Enforce rate limiting by delaying requests if necessary
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.request_delay:
            # Wait the remaining time
            wait_time = self.request_delay - time_since_last_request
            logger.debug(f"Rate limiting: Waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
        
        # Update the last request time
        self.last_request_time = time.time()
    
    def _make_request_with_retries(
        self, 
        params: Dict[str, Any], 
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Make a request to the Bing Image Search API with retries
        
        Args:
            params: Request parameters
            headers: Request headers
            
        Returns:
            Dict: The response data
            
        Raises:
            RequestException: If all retry attempts fail
        """
        last_exception = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Making request (attempt {attempt}/{self.max_retries})")
                response = requests.get(
                    self.endpoint,
                    params=params,
                    headers=headers,
                    timeout=30  # 30 second timeout
                )
                
                # Check for HTTP errors
                response.raise_for_status()
                
                # Parse JSON response
                return response.json()
                
            except RequestException as e:
                last_exception = e
                logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")
                
                if attempt < self.max_retries:
                    # Calculate exponential backoff wait time (1s, 2s, 4s, ...)
                    wait_time = 2 ** (attempt - 1)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        
        # If we get here, all retries failed
        logger.error(f"All {self.max_retries} request attempts failed")
        raise last_exception or RequestException("All retry attempts failed")
