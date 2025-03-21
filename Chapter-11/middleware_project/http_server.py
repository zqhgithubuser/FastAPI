import http.server
import json
import socketserver

from colorama import Back, Fore


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def not_allow_method(self):
        self.send_response(403)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"405 Method Not Allowed")

    def do_POST(self):
        if self.path == "/fastapi-webhook":
            content_length = int(self.headers.get("Content-Length", 0))
            event = json.loads(self.rfile.read(content_length).decode("utf-8"))

            host = event.get("host")
            path = event.get("path")
            timestamp = event.get("time")
            body = event.get("body")

            print(f"{Back.CYAN}time{Back.RESET}: {Fore.CYAN}{timestamp}{Fore.CYAN}")
            print(f"{Back.RED}host{Back.RESET}: {Fore.RED}{host}{Fore.RESET}")
            print(f"{Back.BLUE}path{Back.RESET}: {Fore.BLUE}{path}{Fore.RESET}")
            print(
                f"{Back.LIGHTBLACK_EX}body{Back.RESET}: {Fore.LIGHTBLACK_EX}{body}{Fore.RESET}\n"
            )

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'{"status": "success"}')
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_GET(self):
        self.not_allow_method()

    def do_PUT(self):
        self.not_allow_method()

    def do_DELETE(self):
        self.not_allow_method()

    def do_PATCH(self):
        self.not_allow_method()

    def do_HEAD(self):
        self.not_allow_method()

    def do_OPTIONS(self):
        self.not_allow_method()


def run_server():
    HOST = "localhost"
    PORT = 8080
    Handler = RequestHandler

    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
