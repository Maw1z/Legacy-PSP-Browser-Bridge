from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

PORT = 8888

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        target = self.path

        print(f"[PROXY] GET {target}")

        try:
            if target.startswith("http://"):
                upstream_url = target.replace("http://", "https://", 1)
            else:
                upstream_url = target

            response = requests.get(
                upstream_url,
                headers={
                    "User-Agent": "Mozilla/5.0 Legacy PSP Browser Bridge/1.0",
                    "Accept": "text/html,application/xhtml+xml,*/*",
                },
                timeout=15,
                verify=True,
                allow_redirects=True
            )

            content_type = response.headers.get("Content-Type", "text/html")
            body = response.content

            self.send_response(response.status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception as error:
            print(f"[ERROR] {error}")
            try:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b"Proxy error")
            except Exception:
                pass

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        print(f"[INTERCEPT] POST {self.path}")
        print(f"[INTERCEPT] {body.decode('utf-8', errors='replace')}")

        target = self.path
        if target.startswith("http://"):
            upstream_url = target.replace("http://", "https://", 1)
        else:
            upstream_url = target

        try:
            response = requests.post(
                upstream_url,
                data=body,
                headers={
                    "User-Agent": "Mozilla/5.0 Legacy PSP Browser Bridge/1.0",
                    "Content-Type": self.headers.get("Content-Type", "application/x-www-form-urlencoded"),
                },
                timeout=15,
                verify=True,
                allow_redirects=True
            )

            content_type = response.headers.get("Content-Type", "text/html")
            resp_body = response.content

            self.send_response(response.status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)

        except Exception as error:
            print(f"[ERROR] {error}")
            try:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b"Proxy error")
            except Exception:
                pass

    def log_message(self, format, *args):
        pass

def main():
    server = HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"[PROXY] Listening on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()