import re
from urllib.parse import urlparse

def normalize_username(value):
    if not value:
        return ""

    value = str(value).strip().lower()

    if value.startswith("@"):
        value = value[1:]

    return value

def normalize_name(value):
    if not value:
        return ""

    value = str(value).lower().strip()
    value = re.sub(r"\s+", " ", value)

    return value

def extract_urls(value):
    if not value:
        return []

    urls = re.findall(
        r"https?://[^\s<>'\"]+",
        str(value)
    )

    return [url.rstrip(".,;:!?)]}") for url in urls]

def get_domain(url):
    try:
        hostname = urlparse(url).hostname

        if hostname:
            return hostname.lower().removeprefix("www.")

    except ValueError:
        pass

    return None

def username_variants(username):
    username = normalize_username(username)

    if not username:
        return set()

    variants = {
        username,
        username.replace("_", ""),
        username.replace("-", ""),
        username.replace(".", "")
    }

    compact = re.sub(r"[_\-.]+", "", username)

    if compact:
        variants.add(compact)

    return variants

def correlate(input_username, results):
    target = normalize_username(input_username)
    variants = username_variants(target)

    accounts = []
    links = set()
    domains = set()
    names = set()
    evidence = []

    for platform, data in results.items():
        if not data:
            continue

        username = normalize_username(
            data.get("username") or data.get("login")
        )

        display_name = normalize_name(
            data.get("display_name") or data.get("name")
        )

        profile_url = data.get("profile_url") or data.get("canonical_url")

        if username:
            accounts.append({
                "platform": platform,
                "username": username,
                "url": profile_url
            })

            if username == target:
                evidence.append({
                    "platform": platform,
                    "type": "exact_username",
                    "value": username,
                    "score": 50,
                    "url": profile_url
                })

            elif username in variants:
                evidence.append({
                    "platform": platform,
                    "type": "username_variant",
                    "value": username,
                    "score": 30,
                    "url": profile_url
                })

        if display_name:
            names.add(display_name)

        for key in (
            "profile_url",
            "canonical_url",
            "website"
        ):
            value = data.get(key)

            if value:
                for url in extract_urls(value):
                    links.add(url)

        for key in (
            "bio",
            "description",
            "page_title"
        ):
            value = data.get(key)

            if value:
                for url in extract_urls(value):
                    links.add(url)

    for url in links:
        domain = get_domain(url)

        if domain:
            domains.add(domain)

    for domain in sorted(domains):
        matching_platforms = []

        for platform, data in results.items():
            if not data:
                continue

            for key in (
                "website",
                "profile_url",
                "canonical_url"
            ):
                value = data.get(key)

                if value:
                    for url in extract_urls(value):
                        if get_domain(url) == domain:
                            matching_platforms.append(platform)

        matching_platforms = sorted(set(matching_platforms))

        if len(matching_platforms) >= 2:
            evidence.append({
                "platform": ", ".join(matching_platforms),
                "type": "shared_public_domain",
                "value": domain,
                "score": 40
            })

    score = min(
        100,
        sum(item.get("score", 0) for item in evidence)
    )

    if score >= 80:
        confidence = "HIGH"
    elif score >= 50:
        confidence = "MEDIUM"
    elif score > 0:
        confidence = "LOW"
    else:
        confidence = "NONE"

    return {
        "target": target,
        "accounts": accounts,
        "public_links": sorted(links),
        "domains": sorted(domains),
        "display_names": sorted(names),
        "evidence": evidence,
        "score": score,
        "confidence": confidence
      }
