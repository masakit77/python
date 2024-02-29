import subprocess
import time

def execute_curl(url):
    try:
        output = subprocess.check_output(['curl', url, '-o', '/dev/null', '-w', '%{http_code}\n', '-s'])
        http_code = output.decode().strip()
        return http_code
    except Exception as e:
        print(f"Error connecting to {url}: {e}")
        return None

def main():
    urls = [
            "https://example1.xyz",
            "https://example2.xyz"
    ]
    while True:
        for url in urls:
            http_code = execute_curl(url)
            if http_code is not None:
                print(f"{url} | HTTP response code: {http_code}")
            else:
                print(f"{url} | HTTP response code: N/A")
        time.sleep(1)

if __name__ == "__main__":
    main()
