from modules.platforms import github, reddit, instagram, tiktok, youtube, x, twitch
from modules.correlation import correlate

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

def print_generic(data):
    for key, value in data.items():
        if isinstance(value, list):
            print(f"\n{key.replace('_', ' ').title()}")

            for item in value:
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

def scan_all(username):
    results = {}

    for key, (name, search) in PLATFORMS.items():
        print(f"[>] Checking {name}...")

        try:
            result = search(username)
            results[name] = result

            if result:
                print(f"[+] {name}: public information found")
            else:
                print(f"[-] {name}: not found")

        except Exception as error:
            print(f"[!] {name}: {error}")
            results[name] = None

    return results

def username_menu():
    print("\nSelect platform\n")

    for key, (name, _) in PLATFORMS.items():
        print(f"[{key}] {name}")

    print("[8] All Platforms")
    print("[9] Back")

    choice = input("\nPlatform > ").strip()

    if choice == "9":
        return

    username = input("\nUsername > ").strip().lstrip("@")

    if not username:
        print("Username cannot be empty.")
        return

    if choice == "8":
        print("\nScanning public profiles...\n")

        results = scan_all(username)

        correlation = correlate(username, results)

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
