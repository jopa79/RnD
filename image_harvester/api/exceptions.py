"""
Exception classes for the Bing Image Search API
"""

class BingAPIError(Exception):
    """Base exception for Bing API errors"""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class BingAuthenticationError(BingAPIError):
    """Authentication error with the Bing API (e.g., invalid API key)"""
    pass

class BingRateLimitError(BingAPIError):
    """Rate limit exceeded for the Bing API"""
    pass

class BingSearchError(BingAPIError):
    """Error while searching with the Bing API"""
    pass

def handle_bing_error(status_code, response_data):
    """
    Determine the appropriate error based on status code and response data
    
    Args:
        status_code: HTTP status code
        response_data: Response data from the API (if any)
        
    Returns:
        BingAPIError: The appropriate exception type
    """
    error_message = "Unknown Bing API error"
    
    # Try to extract error message from response if available
    if isinstance(response_data, dict) and 'error' in response_data:
        error_data = response_data['error']
        if 'message' in error_data:
            error_message = error_data['message']
    
    # Determine appropriate exception type based on status code
    if status_code == 401:
        return BingAuthenticationError("Authentication failed: " + error_message, status_code, response_data)
    elif status_code == 429:
        return BingRateLimitError("Rate limit exceeded: " + error_message, status_code, response_data)
    else:
        return BingSearchError(f"Search error ({status_code}): " + error_message, status_code, response_data)
