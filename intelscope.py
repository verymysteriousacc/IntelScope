import os

def clear():
    os.system("clear")

def banner():
    print("""
╔════════════════════════════════╗
║          IntelScope             ║
║      Public OSINT Toolkit       ║
╚════════════════════════════════╝
""")

def menu():
    print("[1] Username Search")
    print("[2] Domain Lookup")
    print("[3] IP Lookup")
    print("[4] URL Analysis")
    print("[5] Exit")

def main():
    while True:
        clear()
        banner()
        menu()

        choice = input("\nIntelScope > ").strip()

        if choice == "1":
            username = input("Username > ").strip()
            print(f"\nSearching public sources for: {username}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            domain = input("Domain > ").strip()
            print(f"\nLooking up public information for: {domain}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            ip = input("IP > ").strip()
            print(f"\nLooking up public information for: {ip}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            url = input("URL > ").strip()
            print(f"\nAnalyzing public information for: {url}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            input("\nInvalid option. Press Enter to continue...")

if __name__ == "__main__":
    main()
