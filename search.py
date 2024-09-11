from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from database import Database

class SearchHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/search'):
            self.handle_search()
        else:
            super().do_GET()

    def handle_search(self):
        query = parse_qs(urlparse(self.path).query).get('query', [''])[0]
        db = Database()
        results = db.search_products(query)
        db.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results).encode())

def run(server_class=HTTPServer, handler_class=SearchHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()