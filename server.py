#PROGRAMA PRINCIPAL
import socketserver
import web

##
#WEB SERVER
##

PORT=8000#A partir de 1024

#Handler=http.server.SimpleHTTPRequestHandler
Handler=web.testHTTPRequestHandler

httpd=socketserver.TCPServer(('',PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

#Handler es la clase a traves de la cual vamos a crear los objetos de las peticiones
#cat fichero.py para verlo en python
