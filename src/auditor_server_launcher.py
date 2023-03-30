from http.server import HTTPServer
from RequestHandler import RequestHandler

if __name__ == '__main__':
    # Define the server address
    server_address = ('localhost', 8000)

    # Create the HTTP server
    httpd = HTTPServer(server_address, RequestHandler)

    # Start the server
    print(f"Starting server on http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()
