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
    profile_url = f"https://www.reddit.com/user/{username}/about.json"
    data = get(profile_url)

    if not data or "data" not in data:
        return None

    user = data["data"]

    result = {
        "username": user.get("name"),
        "profile_url": f"https://www.reddit.com/user/{username}/",
        "account_id": user.get("id"),
        "link_karma": user.get("link_karma"),
        "comment_karma": user.get("comment_karma"),
        "total_karma": user.get("total_karma"),
        "verified": user.get("verified"),
        "created": user.get("created_utc"),
        "is_gold": user.get("is_gold"),
        "is_mod": user.get("is_mod")
    }

    activity_url = f"https://www.reddit.com/user/{username}/submitted.json?limit=25"
    activity = get(activity_url)

    if activity and activity.get("data"):
        posts = []

        for item in activity["data"].get("children", []):
            post = item.get("data", {})

            posts.append({
                "title": post.get("title"),
                "subreddit": post.get("subreddit"),
                "score": post.get("score"),
                "comments": post.get("num_comments"),
                "url": post.get("url"),
                "permalink": (
                    "https://www.reddit.com"
                    + post.get("permalink", "")
                ),
                "created": post.get("created_utc")
            })

        result["public_posts"] = posts

    comments_url = f"https://www.reddit.com/user/{username}/comments.json?limit=25"
    comments = get(comments_url)

    if comments and comments.get("data"):
        comment_list = []

        for item in comments["data"].get("children", []):
            comment = item.get("data", {})

            comment_list.append({
                "subreddit": comment.get("subreddit"),
                "score": comment.get("score"),
                "body": comment.get("body"),
                "permalink": (
                    "https://www.reddit.com"
                    + comment.get("permalink", "")
                ),
                "created": comment.get("created_utc")
            })

        result["public_comments"] = comment_list

    return result
