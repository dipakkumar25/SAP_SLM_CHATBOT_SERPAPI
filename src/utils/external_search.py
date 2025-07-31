import requests
from typing import List, Dict, Any
from ..config.settings import settings

class ExternalSearcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.SERPAPI_KEY
    
    def search(self, query: str, num_results: int = 3) -> List[str]:
        """Search using SerpAPI."""
        if not self.api_key:
            return ["External search failed: API key not configured"]
        
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
                "num": num_results
            }
            
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            
            results = response.json().get("organic_results", [])
            return [f"{res['title']}: {res['link']}" for res in results]
            
        except Exception as e:
            return [f"External search failed: {str(e)}"]