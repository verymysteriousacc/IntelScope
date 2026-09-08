import requests

HEADERS = {
    "User-Agent": "IntelScope/1.0 (Public OSINT Research)"
}

def get(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()

def search(username):
    username = username.strip().lstrip("@")

    try:
        response = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            headers={
                **HEADERS,
                "Content-Type": "application/json"
            },
            json={
                "usernames": [username],
                "excludeBannedUsers": False
            },
            timeout=10
        )

        if response.status_code != 200:
            return None

        users = response.json().get("data", [])

        if not users:
            return None

        user = users[0]
        user_id = user.get("id")

        details = get(f"https://users.roblox.com/v1/users/{user_id}")

        result = {
            "username": user.get("name"),
            "display_name": user.get("displayName"),
            "user_id": user_id,
            "profile_url": f"https://www.roblox.com/users/{user_id}/profile"
        }

        if details:
            result.update({
                "description": details.get("description"),
                "created": details.get("created"),
                "is_banned": details.get("isBanned"),
                "verified": details.get("hasVerifiedBadge")
            })

        avatar = get(
            f"https://thumbnails.roblox.com/v1/users/avatar-headshot"
            f"?userIds={user_id}&size=150x150&format=Png"
        )

        if avatar and avatar.get("data"):
            result["avatar_url"] = avatar["data"][0].get("imageUrl")

        groups = get(
            f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
        )

        if groups:
            result["groups"] = []

            for item in groups.get("data", []):
                group = item.get("group", {})
                role = item.get("role", {})

                result["groups"].append({
                    "name": group.get("name"),
                    "id": group.get("id"),
                    "role": role.get("name"),
                    "group_url": (
                        f"https://www.roblox.com/communities/"
                        f"{group.get('id')}"
                    )
                })

        return result

    except (requests.RequestException, ValueError):
        return None
