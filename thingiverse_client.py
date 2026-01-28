"""
Thingiverse API Client

A Python client for interacting with the Thingiverse API.
Provides methods to search things, get thing details, download files, and more.
"""

import requests
from typing import Optional, List, Dict, Any
import os


class ThingiverseClient:
    """Client for Thingiverse API"""
    
    BASE_URL = "https://api.thingiverse.com"
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize the client.
        
        Args:
            access_token: Access token for API authentication.
                         If not provided, will try to get from THINGIVERSE_ACCESS_TOKEN env var.
        """
        self.access_token = access_token or os.getenv("THINGIVERSE_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError(
                "Access token required. Provide it directly or set THINGIVERSE_ACCESS_TOKEN env var.\n"
                "Get your token at: https://www.thingiverse.com/developers/getting-started"
            )
        self.session = requests.Session()
    
    def _get_params(self, **kwargs) -> Dict[str, Any]:
        """Get request parameters with access token"""
        params = {"access_token": self.access_token}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return params
    
    def get_newest(
        self, 
        per_page: int = 20, 
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get newest things.
        
        Args:
            per_page: Number of results per page (default: 20)
            page: Page number (default: 1)
            
        Returns:
            List of thing objects
        """
        url = f"{self.BASE_URL}/newest"
        params = self._get_params(per_page=per_page, page=page)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_popular(
        self, 
        per_page: int = 20, 
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get popular things.
        
        Args:
            per_page: Number of results per page (default: 20)
            page: Page number (default: 1)
            
        Returns:
            List of thing objects
        """
        url = f"{self.BASE_URL}/popular"
        params = self._get_params(per_page=per_page, page=page)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_thing(self, thing_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific thing.
        
        Args:
            thing_id: Thing ID
            
        Returns:
            Dictionary with thing details
        """
        url = f"{self.BASE_URL}/things/{thing_id}"
        params = self._get_params()
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_thing_files(self, thing_id: int) -> List[Dict[str, Any]]:
        """
        Get files for a specific thing.
        
        Args:
            thing_id: Thing ID
            
        Returns:
            List of file objects with name, url, download_url, size, etc.
        """
        url = f"{self.BASE_URL}/things/{thing_id}/files"
        params = self._get_params()
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_thing_images(self, thing_id: int) -> List[Dict[str, Any]]:
        """
        Get images for a specific thing.
        
        Args:
            thing_id: Thing ID
            
        Returns:
            List of image objects
        """
        url = f"{self.BASE_URL}/things/{thing_id}/images"
        params = self._get_params()
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_thing_tags(self, thing_id: int) -> List[Dict[str, Any]]:
        """
        Get tags for a specific thing.
        
        Args:
            thing_id: Thing ID
            
        Returns:
            List of tag objects
        """
        url = f"{self.BASE_URL}/things/{thing_id}/tags"
        params = self._get_params()
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def search_things(
        self, 
        query: str, 
        per_page: int = 20, 
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search for things by query string.
        
        Args:
            query: Search query string
            per_page: Number of results per page (default: 20)
            page: Page number (default: 1)
            
        Returns:
            List of thing objects matching the query
        """
        url = f"{self.BASE_URL}/search/{query}"
        params = self._get_params(per_page=per_page, page=page)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user(self, username: str) -> Dict[str, Any]:
        """
        Get user profile information.
        
        Args:
            username: Thingiverse username
            
        Returns:
            Dictionary with user profile details
        """
        url = f"{self.BASE_URL}/users/{username}"
        params = self._get_params()
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user_things(
        self, 
        username: str, 
        per_page: int = 20, 
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get things by a specific user.
        
        Args:
            username: Thingiverse username
            per_page: Number of results per page (default: 20)
            page: Page number (default: 1)
            
        Returns:
            List of thing objects
        """
        url = f"{self.BASE_URL}/users/{username}/things"
        params = self._get_params(per_page=per_page, page=page)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def download_file(self, file_url: str, save_path: str) -> None:
        """
        Download a file from Thingiverse.
        
        Args:
            file_url: URL from file object's download_url or url field
            save_path: Local path to save the file
        """
        # Add access token to file download URL if not present
        if "access_token" not in file_url:
            separator = "&" if "?" in file_url else "?"
            file_url = f"{file_url}{separator}access_token={self.access_token}"
        
        response = self.session.get(file_url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
