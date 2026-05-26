import json
import sys
import urllib.error
import urllib.request


DEFAULT_PAYLOAD = {
    "messages": [
        "REQUIRED 1 BHK FLAT FOR OUT RATE BUDGET 1 CR TO 1.10 CR",
        "LOCATION ANY CHARKOP SECTOR KANDIVALI WEST",
    ]
}


def main():
    if len(sys.argv) > 1:
        payload = {"messages": sys.argv[1:]}
    else:
        payload = DEFAULT_PAYLOAD

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        "http://127.0.0.1:8000/extract",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            print(body)
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}")
        print(error.read().decode("utf-8"))
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"Request failed: {error.reason}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()