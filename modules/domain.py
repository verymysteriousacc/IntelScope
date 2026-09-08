import socket
import requests

def dns_lookup(domain):
    results = {}

    try:
        results["IPv4"] = socket.gethostbyname_ex(domain)[2]
    except socket.gaierror:
        results["IPv4"] = []

    try:
        results["Hostname"] = socket.getfqdn(domain)
    except Exception:
        results["Hostname"] = None

    return results

def rdap_lookup(domain):
    url = f"https://rdap.org/domain/{domain}"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "IntelScope/1.0"},
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "handle": data.get("handle"),
            "name": data.get("ldhName"),
            "status": data.get("status", []),
            "nameservers": [
                ns.get("ldhName")
                for ns in data.get("nameservers", [])
                if ns.get("ldhName")
            ]
        }

    except (requests.RequestException, ValueError):
        return None

def domain_lookup(domain):
    domain = domain.strip().lower()

    return {
        "dns": dns_lookup(domain),
        "rdap": rdap_lookup(domain)
      }
