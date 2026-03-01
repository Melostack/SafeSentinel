import requests

def test_cors_vulnerability():
    url = "http://localhost:8000/"

    # Check 1: Unauthorized Origin
    headers_unauth = {
        "Origin": "http://evil-site.com"
    }
    try:
        response_unauth = requests.get(url, headers=headers_unauth)
        allow_origin_unauth = response_unauth.headers.get('access-control-allow-origin')
        print(f"Unauthorized Request - Origin: {headers_unauth['Origin']}")
        print(f"Status Code: {response_unauth.status_code}")
        print(f"Access-Control-Allow-Origin: {allow_origin_unauth}")

        if allow_origin_unauth is None or allow_origin_unauth != headers_unauth['Origin']:
             print("SECURE: Access-Control-Allow-Origin is restricted for unauthorized origin.")
        else:
             print("VULNERABLE: allowed origin is present for unauthorized origin")

    except requests.exceptions.ConnectionError:
        print("Could not connect to server for unauthorized check. Make sure it is running.")
        return

    # Check 2: Authorized Origin
    headers_auth = {
        "Origin": "http://localhost:3000"
    }
    try:
        response_auth = requests.get(url, headers=headers_auth)
        allow_origin_auth = response_auth.headers.get('access-control-allow-origin')
        print(f"\nAuthorized Request - Origin: {headers_auth['Origin']}")
        print(f"Status Code: {response_auth.status_code}")
        print(f"Access-Control-Allow-Origin: {allow_origin_auth}")

        if allow_origin_auth == headers_auth['Origin']:
            print("SUCCESS: Authorized origin is allowed.")
        else:
            print("FAILURE: Authorized origin is NOT allowed.")

    except requests.exceptions.ConnectionError:
        print("Could not connect to server for authorized check. Make sure it is running.")

if __name__ == "__main__":
    test_cors_vulnerability()
