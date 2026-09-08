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

    for key, value in result.items():
        if value is not None:
            print(f"{key.title()}: {value}")
