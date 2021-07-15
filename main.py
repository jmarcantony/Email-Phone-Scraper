try:
    import os
    import re
    import sys
    import requests
    import validators
except ModuleNotFoundError:
    print("[-] Requirements not satisfied!\n\trun 'pip install -r requirements.txt'\n\t\tOR\n\trun 'pip3 install -r requirements.txt'")
    quit()

def print_docs():
    docs = f"""
    Documentation:
        Base Usage: {"python" if os.name == "nt" else "python3"} {sys.argv[0]} [URL] [FLAGS]

        Flags:
            -a:
                Gets Phone Numbers & Email Adresses from the URL
            -e:
                Gets Only Email Adresses from the URL
            -p:
                Gets Only Phone Numbers from the URL
            -O [FILENAME]:
                Saves Scraped Data to a file.
    """
    print(docs)

def log(data, filename):
    with open(filename, "a") as f:
        for info in data:
            f.write(f"{info}\n")

def harvest_emails(url, saveEmails=False, filename=None):
    try:
        r = requests.get(url)
    except:
        print("[-] The requested URL did not respond back")
        sys.exit()
    
    data = r.text
    
    pattern = r"([\d\w\.]+@[\d\w\.\-]+\.\w+)"
    
    if re.search(pattern, data):
        emails = set(re.findall(pattern, data))
        for email in emails:
            print(f"[+] Email Found: {email}")
        print(f"[*] Found {len(emails)} emails\n")
        if saveEmails:
            log(emails, filename)
            print(f"[*] Saved Harvested Emails in '{filename}'\n")
    else:
        print("[-] Did not find any valid emails")

def harvest_phones(url, savePhones=False, filename=None):
    try:
        r = requests.get(url)
    except:
        print("[-] The requested URL did not respond back")
        sys.exit()
    
    data = r.text
    
    pattern = r"(\(?[0-9]{3}\)?(?:\-|\s|\.)?[0-9]{3}(?:\-|\.)[0-9]{4})"
    
    if re.search(pattern, data):
        nums = set(re.findall(pattern, data))
        for num in nums:
            print(f"[+] Phone Number Found: {num}")
        print(f"[*] Found {len(nums)} phone numbers\n")
        if savePhones:
            log(nums, filename)
            print(f"[*] Saved Harvested Phone Numbers in '{filename}'\n")
    else:
        print("[-] Did not find any valid phone numbers")

def harvest(url, save=False, filename=None):
    harvest_emails(url, save, filename)
    harvest_phones(url, save, filename)


def main():
    if len(sys.argv) >= 2:
        if "--help" in sys.argv:
            print_docs()
            sys.exit()
        url = sys.argv[1]
        isValid = validators.url(url)
        if isValid:
            if "-a" in sys.argv:
                if "-O" in sys.argv:
                    try:
                        filename = sys.argv[sys.argv.index("-O") + 1]
                    except IndexError:
                        print("[-] Please provide a valid filename")
                        sys.exit()
                    harvest(url, True, filename)
                else:
                    harvest(url)
            elif "-e" in sys.argv:
                if "-O" in sys.argv:
                    try:
                        filename = sys.argv[sys.argv.index("-O") + 1]
                    except IndexError:
                        print("[-] Please provide a valid filename")
                        sys.exit()
                    harvest_emails(url, True, filename)
                else:
                    harvest_emails(url)
            elif "-p" in sys.argv:
                if "-O" in sys.argv:
                    try:
                        filename = sys.argv[sys.argv.index("-O") + 1]
                    except IndexError:
                        print("[-] Please provide a valid filename")
                        sys.exit()
                    harvest_phones(url, True, filename)
                else:
                    harvest_phones(url)
            else:
                print(f"[-] Please provide a valid flag operation")
        else:
            print(f"[-] Invalid URL")
            sys.exit()
    else:
        print(f"[-] Invalid Usage:\n\tUsage: {'python' if os.name == 'nt' else 'python3'} {sys.argv[0]} [URL] [FLAGS]")
        print(f"\tTry '{'python' if os.name == 'nt' else 'python3'} {sys.argv[0]} --help' for help")
        sys.exit()

if __name__ == "__main__":
    main()
