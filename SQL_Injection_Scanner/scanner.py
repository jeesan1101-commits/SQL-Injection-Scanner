import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time

ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated"
]

def load_payloads():
    with open("payloads.txt", "r") as f:
        return f.read().splitlines()

def scan_url(url, payloads):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        print("[-] No parameters found")
        return

    for param in params:
        for payload in payloads:
            test_params = params.copy()
            test_params[param] = payload

            new_query = urlencode(test_params, doseq=True)
            test_url = urlunparse(parsed._replace(query=new_query))

            try:
                response = requests.get(test_url, timeout=5)
                for error in ERRORS:
                    if error.lower() in response.text.lower():
                        print(f"[VULNERABLE] {test_url}")
                        with open("report.txt", "a") as report:
                            report.write(f"Vulnerable URL: {test_url}\n")
                        break
                time.sleep(1)
            except requests.exceptions.RequestException:
                pass

if __name__ == "__main__":
    target = input("Enter target URL: ")
    payloads = load_payloads()
    scan_url(target, payloads)