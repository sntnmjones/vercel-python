from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))
        return

    def do_POST(self):
        try:
            # Get the post body length
            content_len = int(self.headers.get('Content-Length', 0))
            if content_len <= 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Content-Length must be greater than 0')
                return

            post_body = self.rfile.read(content_len).decode('utf-8')

            # Decode the post_body and handle potential decoding errors
            try:
                response_message = "received post request:<br>{}".format(post_body)
            except UnicodeDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid UTF-8 encoding')
                return

            self.send_response(200)  # Send the response before writing to wfile
            self.send_header('Content-type', 'text/html')  # Set the content type
            self.end_headers()
            self.wfile.write(response_message.encode('utf-8'))  # Encode str to bytes
        except Exception as e:
            self.send_response(500)  # Internal Server Error
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
            