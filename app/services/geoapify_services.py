import os
import requests

class GeoapifyService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEOAPIFY_API_KEY")
        self.base_url = "https://api.geoapify.com/v1/geocode/reverse"

    def reverse_geocode(self, lat: float, lon: float) -> str:
        if not self.api_key:
            return "an unknown location"

        url = f"{self.base_url}?lat={lat}&lon={lon}&apiKey={self.api_key}"
        headers = {"Accept": "application/json"}
        
        try:
            resp = requests.get(url, headers=headers)

            if resp.status_code == 200:
                data = resp.json()
                features = data.get("features", [])
                if not features:
                    return "an unknown location"

                props = features[0].get("properties", {})

                # Prefer formatted address
                if "formatted" in props:
                    return props["formatted"]

                # Fallback manual formatting
                parts = [
                    props.get("name"),
                    props.get("street"),
                    props.get("housenumber"),
                    props.get("postcode"),
                    props.get("city"),
                    props.get("country")
                ]
                return ", ".join(filter(None, parts)) or "an unknown location"

            return "an unknown location"
        except Exception as e:
            print(e)
            return "an unknown location"