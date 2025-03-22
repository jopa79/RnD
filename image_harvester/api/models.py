"""
Data models for the Bing Image Search API
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

@dataclass
class ImageMetadata:
    """Metadata for an image from Bing Image Search"""
    content_url: str
    name: str
    width: int
    height: int
    content_size: Optional[int] = None
    encoding_format: Optional[str] = None
    host_page_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_date: Optional[datetime] = None
    content_type: Optional[str] = None
    accentColor: Optional[str] = None
    
    # Raw data for any other properties not explicitly defined
    _raw_data: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageMetadata':
        """
        Create an ImageMetadata instance from a dictionary
        
        Args:
            data: Dictionary containing image metadata from Bing
            
        Returns:
            ImageMetadata: Instance populated with the data
        """
        # Required fields
        content_url = data.get('contentUrl', '')
        name = data.get('name', '')
        width = data.get('width', 0)
        height = data.get('height', 0)
        
        # Optional fields
        content_size = data.get('contentSize', None)
        if content_size is not None and isinstance(content_size, str):
            # Convert string like "1234 B" to int
            if ' B' in content_size:
                content_size = int(content_size.split(' B')[0])
        
        encoding_format = data.get('encodingFormat', None)
        host_page_url = data.get('hostPageUrl', None)
        thumbnail_url = data.get('thumbnailUrl', None)
        
        # Parse date if available
        created_date = None
        if 'datePublished' in data:
            try:
                created_date = datetime.fromisoformat(data['datePublished'].rstrip('Z'))
            except (ValueError, TypeError):
                pass
        
        content_type = data.get('contentType', None)
        accent_color = data.get('accentColor', None)
        
        # Store the original data
        return cls(
            content_url=content_url,
            name=name,
            width=width,
            height=height,
            content_size=content_size,
            encoding_format=encoding_format,
            host_page_url=host_page_url,
            thumbnail_url=thumbnail_url,
            created_date=created_date,
            content_type=content_type,
            accentColor=accent_color,
            _raw_data=data
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the ImageMetadata to a dictionary
        
        Returns:
            Dict: Dictionary representation of the metadata
        """
        return {
            'content_url': self.content_url,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'content_size': self.content_size,
            'encoding_format': self.encoding_format,
            'host_page_url': self.host_page_url,
            'thumbnail_url': self.thumbnail_url,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'content_type': self.content_type,
            'accent_color': self.accentColor,
        }
    
    def to_json(self) -> str:
        """
        Convert the ImageMetadata to a JSON string
        
        Returns:
            str: JSON string representation of the metadata
        """
        return json.dumps(self.to_dict(), default=str)
    
    def meets_size_requirements(self, min_width: int, min_height: int) -> bool:
        """
        Check if the image meets the minimum size requirements
        
        Args:
            min_width: Minimum width in pixels
            min_height: Minimum height in pixels
            
        Returns:
            bool: True if the image meets the size requirements
        """
        return self.width >= min_width and self.height >= min_height

@dataclass
class SearchResult:
    """Result of a Bing Image Search"""
    query: str
    images: List[ImageMetadata]
    next_offset: Optional[int] = None
    total_estimated_matches: int = 0
    
    @classmethod
    def from_response(cls, query: str, response_data: Dict[str, Any]) -> 'SearchResult':
        """
        Create a SearchResult from the Bing Image Search API response
        
        Args:
            query: The search query used
            response_data: The API response data
            
        Returns:
            SearchResult: Instance populated with the response data
        """
        images = []
        value = response_data.get('value', [])
        
        for item in value:
            try:
                image = ImageMetadata.from_dict(item)
                images.append(image)
            except Exception as e:
                print(f"Error parsing image: {e}")
        
        # Get pagination information
        next_offset = None
        if 'nextOffset' in response_data:
            next_offset = response_data['nextOffset']
        
        total_estimated_matches = response_data.get('totalEstimatedMatches', 0)
        
        return cls(
            query=query,
            images=images,
            next_offset=next_offset,
            total_estimated_matches=total_estimated_matches
        )
    
    def filter_by_size(self, min_width: int, min_height: int) -> 'SearchResult':
        """
        Filter images by size
        
        Args:
            min_width: Minimum width in pixels
            min_height: Minimum height in pixels
            
        Returns:
            SearchResult: New SearchResult with filtered images
        """
        filtered_images = [
            img for img in self.images 
            if img.meets_size_requirements(min_width, min_height)
        ]
        
        return SearchResult(
            query=self.query,
            images=filtered_images,
            next_offset=self.next_offset,
            total_estimated_matches=self.total_estimated_matches
        )
