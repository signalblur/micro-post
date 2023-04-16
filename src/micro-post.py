import sys
import argparse
import requests
import json

def main():
    parser = argparse.ArgumentParser(description="Fetch a URL and display the response attributes.")
    parser.add_argument("url", help="The URL to fetch.")
    parser.add_argument("--status", "-s", action="store_true", help="Display the status code.")
    parser.add_argument("--headers", "-H", action="store_true", help="Display the headers.")
    parser.add_argument("--text", "-t", action="store_true", help="Display the response text.")
    parser.add_argument("--json", "-j", action="store_true", help="Display the JSON response.")

    args = parser.parse_args()

    url = args.url
    if not (url.startswith('http://') or url.startswith('https://')):
        url = f'http://{url}'

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

    any_flag_set = any([args.status, args.headers, args.text, args.json])

    if not any_flag_set or args.status:
        print(f"{response.status_code}")

    if not any_flag_set or args.headers:
        print(f"{json.dumps(dict(response.headers), indent=2)}")

    if not any_flag_set or args.text:
        print(f"{response.text}")

    if not any_flag_set or args.json:
        try:
            json_data = response.json()
            print(f"{json.dumps(json_data, indent=2)}")
        except ValueError:
            if args.json:
                print("Error: No JSON data in the response")

if __name__ == "__main__":
    main()
