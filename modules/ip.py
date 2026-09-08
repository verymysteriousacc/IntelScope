import requests

API_URL = "https://ipwho.is/{}"

def ip_lookup(ip):
    try:
        response = requests.get(
            API_URL.format(ip),
            headers={"User-Agent": "IntelScope/1.0"},
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data.get("success"):
            return None

        return {
            "ip": data.get("ip"),
            "type": data.get("type"),
            "continent": data.get("continent"),
            "country": data.get("country"),
            "region": data.get("region"),
            "city": data.get("city"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "isp": data.get("connection", {}).get("isp"),
            "organization": data.get("connection", {}).get("org"),
            "asn": data.get("connection", {}).get("asn")
        }

    except (requests.RequestException, ValueError):
        return None
