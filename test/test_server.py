from pathlib import Path
from urllib.request import urlopen

from pylage.runtime import LocalServer


output_dir = Path("test_output")

server = LocalServer(output_dir)

try:
    url = server.start()

    print("=== PYLAGE LOCAL SERVER TEST ===")
    print("URL:", url)

    with urlopen(url) as response:
        body = response.read().decode("utf-8")

        print("Status:", response.status)
        print("Content-Type:", response.headers["Content-Type"])
        print("Bytes:", len(body))
        print("HTML:", body[:80].replace("\n", " "))

finally:
    server.stop()

print("Server stopped.")
