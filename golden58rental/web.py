from http.server import HTTPServer,CGIHTTPRequestHandler

PORT = 8000

#创建服务器对象
httpd = HTTPServer(("",PORT),CGIHTTPRequestHandler)
print("serving at port",PORT)

#反复处理连接请求
httpd.serve_forever()

#121.4378499985,31.1928327643
