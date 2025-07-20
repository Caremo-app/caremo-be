import os
import requests
import re

class GeoapifyService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEOAPIFY_API_KEY")
        self.base_url = "https://api.geoapify.com/v1/geocode/reverse"
        self.fallback_types = [
            "&type=amenity", "&type=building", "&type=street",
            "&type=suburb", "&type=postcode", "&type=city",
            "&type=county", "&type=state", "&type=country", ""
        ]

    def _make_request(self, lat, lon, geocode_type):
        url = (
            f"{self.base_url}?lat={lat}&lon={lon}&format=json"
            f"{geocode_type}&lang=id&apiKey={self.api_key}"
        )
        headers = {"Accept": "application/json"}
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"[{geocode_type}] Status code: {resp.status_code}")
        except Exception as e:
            print(f"[{geocode_type}] Request failed:", e)
        return {}

    def reverse_geocode(self, lat: float, lon: float) -> str:
        if not self.api_key:
            print("Missing Geoapify API key")
            return "an unknown location"

        for geocode_type in self.fallback_types:
            data = self._make_request(lat, lon, geocode_type)

            # Determine which response format we're getting
            results = data.get("results") or data.get("features")
            if not results:
                continue

            # Extract top-level props
            item = results[0]
            props = item.get("properties", item)  # if "properties" doesn't exist, use top-level

            # 1. Prefer 'formatted'
            if "formatted" in props and props["formatted"]:
                return props["formatted"]

            # 2. Extract RT/RW if embedded
            rt_rw = ""
            for field in ["street", "name", "address_line1"]:
                val = props.get(field, "")
                match = re.search(r"RT\s*0*\d+\s*/\s*RW\s*0*\d+", val, re.IGNORECASE)
                if match:
                    rt_rw = match.group()
                    break

            # 3. Build manual address
            parts = [
                props.get("housenumber"),
                props.get("street"),
                props.get("suburb") or props.get("village"),   # Kelurahan
                props.get("district"),                          # Kecamatan
                props.get("city"),
                props.get("county"),
                props.get("state"),
                props.get("postcode"),
                props.get("country"),
            ]

            if rt_rw and all(rt_rw not in (p or "") for p in parts):
                parts.insert(2, rt_rw)

            address = ", ".join([p for p in parts if p])
            if address:
                return address

        return "an unknown location"
