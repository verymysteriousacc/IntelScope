from modules.username import search_username

def banner():
    print("""
╔════════════════════════════════╗
║          IntelScope            ║
║      Public OSINT Toolkit      ║
╚════════════════════════════════╝
""")

def username_search():
    username = input("\nUsername > ").strip()

    if not username:
        print("Username cannot be empty.")
        input("\nPress Enter...")
        return

    print(f"\nSearching public profiles for @{username}...\n")

    results = search_username(username)

    for result in results:
        status = result["status"]
        site = result["site"]

        if status == "FOUND":
            print(f"[+] {site}: FOUND")
            print(f"    {result['final_url']}")
        elif status == "NOT FOUND":
            print(f"[-] {site}: NOT FOUND")
        else:
            print(f"[?] {site}: {status}")

    input("\nPress Enter to continue...")

def main():
    while True:
        banner()

        print("[1] Username Search")
        print("[2] Domain Lookup")
        print("[3] IP Lookup")
        print("[4] URL Analysis")
        print("[5] Exit")

        choice = input("\nIntelScope > ").strip()

        if choice == "1":
            username_search()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("\nThat module isn't built yet.")
            input("\nPress Enter...")

if __name__ == "__main__":
    main()
