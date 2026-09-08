from modules.platforms import github, reddit, instagram, tiktok, youtube, x, twitch

PLATFORMS = {
    "1": ("GitHub", github.search),
    "2": ("Reddit", reddit.search),
    "3": ("Instagram", instagram.search),
    "4": ("TikTok", tiktok.search),
    "5": ("YouTube", youtube.search),
    "6": ("X", x.search),
    "7": ("Twitch", twitch.search)
}

def print_value(name, value):
    if value is not None and value != "":
        print(f"{name}: {value}")

def print_github(data):
    print("GitHub")
    print("──────")

    fields = [
        ("Username", "username"),
        ("Display Name", "display_name"),
        ("Bio", "bio"),
        ("Profile URL", "profile_url"),
        ("Avatar URL", "avatar_url"),
        ("Public Repositories", "public_repositories"),
        ("Followers", "followers"),
        ("Following", "following"),
        ("Public Gists", "public_gists"),
        ("Company", "company"),
        ("Location", "location"),
        ("Website", "website"),
        ("Account Created", "account_created"),
        ("Last Updated", "last_updated")
    ]

    for name, key in fields:
        print_value(name, data.get(key))

    repositories = data.get("repositories", [])

    if repositories:
        print("\nRepositories")
        print("────────────")

        for index, repo in enumerate(repositories, 1):
            print(f"\n[{index}] {repo.get('name')}")

            print_value("    Description", repo.get("description"))
            print_value("    URL", repo.get("url"))
            print_value("    Language", repo.get("language"))
            print_value("    Stars", repo.get("stars"))
            print_value("    Forks", repo.get("forks"))
            print_value("    Open Issues", repo.get("open_issues"))
            print_value("    Created", repo.get("created"))
            print_value("    Updated", repo.get("updated"))

    activity = data.get("recent_public_activity", [])

    if activity:
        print("\nRecent Public Activity")
        print("──────────────────────")

        for event in activity:
            print(
                f"{event.get('created')} | "
                f"{event.get('type')} | "
                f"{event.get('repository')}"
            )

def print_generic(data):
    for key, value in data.items():
        if isinstance(value, list):
            print(f"\n{key.replace('_', ' ').title()}")

            for item in value:
                print(f"  • {item}")

        elif value is not None and value != "":
            print(f"{key.replace('_', ' ').title()}: {value}")

def username_menu():
    print("\nSelect platform\n")

    for key, (name, _) in PLATFORMS.items():
        print(f"[{key}] {name}")

    print("[8] Back")

    choice = input("\nPlatform > ").strip()

    if choice == "8":
        return

    if choice not in PLATFORMS:
        print("\nInvalid option.")
        return

    username = input("\nUsername > ").strip().lstrip("@")

    if not username:
        print("Username cannot be empty.")
        return

    name, search = PLATFORMS[choice]

    print(f"\nScanning public {name} information for @{username}...\n")

    try:
        result = search(username)
    except Exception as error:
        print(f"Error: {error}")
        return

    if not result:
        print("No public information found.")
        return

    if name == "GitHub":
        print_github(result)
    else:
        print_generic(result)
