from modules.username import search_username
from modules.domain import domain_lookup
from modules.ip import ip_lookup
from modules.url import analyze_url

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

def url_search():
    url = input("\nURL > ").strip()

    if not url:
        print("URL cannot be empty.")
        pause()
        return

    print(f"\nAnalyzing public URL: {url}\n")

    result = analyze_url(url)

    print(f"URL: {result.get('url')}")
    print(f"Scheme: {result.get('scheme')}")
    print(f"Hostname: {result.get('hostname')}")
    print(f"Port: {result.get('port')}")
    print(f"Path: {result.get('path')}")

    if "status_code" in result:
        print(f"\nHTTP Status: {result['status_code']}")
        print(f"Final URL: {result['final_url']}")
        print(f"Server: {result.get('server')}")
        print(f"Content-Type: {result.get('content_type')}")
        print(f"Content-Length: {result.get('content_length')}")
        print(f"Redirects: {result.get('redirects')}")

        print("\nSecurity Headers")
        print("────────────────")

        for name, value in result["security_headers"].items():
            print(f"{name}: {value or 'Not present'}")

    if "error" in result:
        print(f"\nError: {result['error']}")

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
            url_search()

        elif choice == "5":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid option.")
            pause()

if __name__ == "__main__":
    main()
