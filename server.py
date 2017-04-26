import socketserver
import web

PORT=8000

Handler=web.testHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address=True
httpd=socketserver.TCPServer(('',PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
