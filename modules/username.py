from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.platforms import (
    github,
    reddit,
    instagram,
    tiktok,
    youtube,
    x,
    twitch,
    roblox,
    discord
)

from modules.correlation import correlate

PLATFORMS = {
    "1": ("GitHub", github.search),
    "2": ("Reddit", reddit.search),
    "3": ("Instagram", instagram.search),
    "4": ("TikTok", tiktok.search),
    "5": ("YouTube", youtube.search),
    "6": ("X", x.search),
    "7": ("Twitch", twitch.search),
    "8": ("Roblox", roblox.search),
    "9": ("Discord", discord.search)
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

def print_generic(data):
    for key, value in data.items():
        if isinstance(value, list):
            print(f"\n{key.replace('_', ' ').title()}")

            for item in value:
                if isinstance(item, dict):
                    print()

                    for sub_key, sub_value in item.items():
                        print_value(
                            f"  {sub_key.replace('_', ' ').title()}",
                            sub_value
                        )
                else:
                    print(f"  • {item}")

        elif value is not None and value != "":
            print(f"{key.replace('_', ' ').title()}: {value}")

def print_correlation(data):
    print("\nACCOUNT CORRELATION")
    print("══════════════════")

    print(f"\nTarget: @{data['target']}")
    print(f"Confidence: {data['confidence']}")
    print(f"Correlation Score: {data['score']}/100")

    accounts = data.get("accounts", [])

    if accounts:
        print("\nPUBLIC ACCOUNTS")
        print("───────────────")

        for account in accounts:
            print(
                f"[+] {account['platform']}: "
                f"@{account['username']}"
            )

            if account.get("url"):
                print(f"    {account['url']}")

    names = data.get("display_names", [])

    if names:
        print("\nPUBLIC DISPLAY NAMES")
        print("────────────────────")

        for name in names:
            print(f"• {name}")

    domains = data.get("domains", [])

    if domains:
        print("\nPUBLIC DOMAINS")
        print("──────────────")

        for domain in domains:
            print(f"• {domain}")

    links = data.get("public_links", [])

    if links:
        print("\nPUBLIC LINKS")
        print("────────────")

        for link in links:
            print(f"• {link}")

    evidence = data.get("evidence", [])

    if evidence:
        print("\nCORRELATION EVIDENCE")
        print("────────────────────")

        for item in evidence:
            print(
                f"[{item.get('score', 0)}] "
                f"{item.get('type')} → "
                f"{item.get('value')}"
            )

def scan_platform(platform, search, username):
    try:
        return platform, search(username), None
    except Exception as error:
        return platform, None, str(error)

def scan_all(username):
    results = {}

    with ThreadPoolExecutor(
        max_workers=len(PLATFORMS)
    ) as executor:

        tasks = [
            executor.submit(
                scan_platform,
                name,
                search,
                username
            )
            for name, search in PLATFORMS.values()
        ]

        for task in as_completed(tasks):
            platform, result, error = task.result()

            if error:
                print(f"[!] {platform}: {error}")
                results[platform] = None
                continue

            results[platform] = result

            if result:
                print(
                    f"[+] {platform}: "
                    "public information found"
                )
            else:
                print(
                    f"[-] {platform}: "
                    "not found"
                )

    return results

def username_menu():
    print("\nSelect platform\n")

    for key, (name, _) in PLATFORMS.items():
        print(f"[{key}] {name}")

    print("[10] All Platforms")
    print("[11] Back")

    choice = input("\nPlatform > ").strip()

    if choice == "11":
        return

    username = input(
        "\nUsername > "
    ).strip().lstrip("@")

    if not username:
        print("Username cannot be empty.")
        return

    if choice == "10":
        print(
            "\nScanning public profiles...\n"
        )

        results = scan_all(username)
        correlation = correlate(
            username,
            results
        )

        print_correlation(correlation)

        return

    if choice not in PLATFORMS:
        print("\nInvalid option.")
        return

    name, search = PLATFORMS[choice]

    print(
        f"\nScanning public {name} information "
        f"for @{username}...\n"
    )

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
