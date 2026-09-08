from modules.username import search_username
from modules.domain import domain_lookup
from modules.ip import ip_lookup

def banner():
    print("""
╔════════════════════════════════╗
║          IntelScope            ║
║      Public OSINT Toolkit      ║
╚════════════════════════════════╝
""")

def pause():
    input("\nPress Enter to continue...")

def username_search():
    username = input("\nUsername > ").strip()

    if not username:
        print("Username cannot be empty.")
        pause()
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
        elif status == "RESTRICTED":
            print(f"[!] {site}: RESTRICTED")
        else:
            print(f"[?] {site}: {status}")

    pause()

def domain_search():
    domain = input("\nDomain > ").strip()

    if not domain:
        print("Domain cannot be empty.")
        pause()
        return

    print(f"\nLooking up public information for {domain}...\n")

    results = domain_lookup(domain)

    print("DNS")
    print("───")

    ipv4 = results["dns"].get("IPv4", [])

    if ipv4:
        for ip in ipv4:
            print(f"IPv4: {ip}")
    else:
        print("IPv4: Not found")

    print(f"Hostname: {results['dns'].get('Hostname')}")

    print("\nRDAP")
    print("────")

    rdap = results.get("rdap")

    if rdap:
        print(f"Name: {rdap.get('name')}")
        print(f"Handle: {rdap.get('handle')}")

        statuses = rdap.get("status", [])

        if statuses:
            print(f"Status: {', '.join(statuses)}")

        nameservers = rdap.get("nameservers", [])

        if nameservers:
            print("Nameservers:")

            for ns in nameservers:
                print(f"  • {ns}")
    else:
        print("RDAP information unavailable.")

    pause()

def ip_search():
    ip = input("\nIP > ").strip()

    if not ip:
        print("IP cannot be empty.")
        pause()
        return

    print(f"\nLooking up public information for {ip}...\n")

    result = ip_lookup(ip)

    if not result:
        print("Unable to retrieve public IP information.")
        pause()
        return

    for key, value in result.items():
        if value is not None:
            print(f"{key.title()}: {value}")

    pause()

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

        elif choice == "2":
            domain_search()

        elif choice == "3":
            ip_search()

        elif choice == "4":
            print("\nURL Analysis isn't implemented yet.")
            pause()

        elif choice == "5":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid option.")
            pause()

if __name__ == "__main__":
    main()
