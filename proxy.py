import socket
import threading
import sys
import os
import logging

global timeout

class client_Proxy():
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.threads = []
        self.create_socket()

    def create_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.host, self.port))
            sock.listen(50)
            print("Serving on port " + str(self.port))
            self.sock = sock
            self.accept_req()
        except socket.error as message:
            if sock:
                sock.close()
            print("Could not open socket:" + str(message))
            sys.exit(1)

    def accept_req(self):
        while 1:
            try:
                conn,addr=self.sock.accept()#accept Request
                if conn:
                    thr_multiple=Multiple(conn,addr)
                    thr_multiple.start()
                    self.threads.append(thr_multiple)
                """for elements in self.threads:
                    elements.join()"""
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
                
class Multiple(threading.Thread):
    def __init__(self,conn,addr):
        threading.Thread.__init__(self)
        print("client connected at %s", conn)
        self.conn = conn
        self.addr = addr

    def run(self):
        request = self.conn.recv(65535)
        flag = 1
        flag2 = 1
        if request:
            request2 = request.decode()
            print(request2)
            request3 = request2.split("\n")
            line1 = request3[0].split()
            try:
                line2 = request3[1].split()
                line22 = line2[1].split(":")
                line13 = line1[2].split(":")
                print(line13)
                if line13[0] == "HTTP/1.0":
                    if line1[0] == "GET":
                        pathh = os.getcwd()
                        filee = pathh + "/" + "blocked.txt"
                        fhh = open(filee, "r")
                        dataa = fhh.read()
                        dataa2 = dataa.split()
                        print(line22[0])
                        for linee in dataa2:
                            if line22[0] == linee:
                                header = (line1[2] + " 400 Bad Request\n")
                                cntType = "Content-Type .html text/html"
                                http_response = ("<html><body>400 Bad Request Reason: Cannot be accessed: " + line22[0] + "</body></html>").encode()
                                flag = 0
                                flag2 = 0
                                break
                        if not flag2 == 0:
                            line12 = line1[1].split(":")
                            try:
                                servport = int(line22[1])
                            except:
                                servport = 80
                            servadd = line22[0]
                            if (line1[2] == "http://detectportal.firefox.com/success.txt"):
                                header = (line1[2] + " 400 Bad Request\n")
                                cntType = "Content-Type .html text/html"
                                http_response = ("<html><body>400 Bad Request Reason: Invalid Method: " + line1[0] + "</body></html>").encode()
                                flag = 0
                            else:
                                try:
                                    socket.gethostbyaddr(servadd)
                                    server_proxy(servadd, servport, request, self.conn)
                                    self.conn.close()
                                except Exception as e:
                                    header = (line1[2] + " 400 Bad Request\n")
                                    cntType = "Content-Type .html text/html"
                                    http_response = ("<html><body>400 Bad Request Reason: Invalid URL: " + servadd + "</body></html>").encode()
                                    flag = 0
                                    print("error url not found")
                                    print(e)
                    else:  #if not get what?
                        header = (line1[2] + " 400 Bad Request\n")
                        cntType = "Content-Type .html text/html"
                        http_response = ("<html><body>400 Bad Request Reason: Invalid Method: " + line1[0] + "</body></html>").encode()
                        flag = 0
                else:
                    header = (line1[2] + " 400 Bad Request\n")
                    cntType = "Content-Type .html text/html"
                    http_response = ("<html><body>400 Bad Request Reason: Invalid HTTP-Version: " + line1[3] + "</body></html>").encode()
                    flag = 0
                    print("not a proper request like http")
                if flag == 0:
                    cnt = cntType.split()
                    header2 = (cnt[0] + ": " + cnt[2] + "\n")
                    print(header)
                    print(header2)
                    print(http_response)
                    self.conn.send(header.encode())
                    self.conn.send(header2.encode())
                    self.conn.send(b'\n')
                    self.conn.send(http_response)
                    self.conn.close()
            except:
                header = (line1[2] + " 503 Service Unavailable\n")
                cntType = "Content-Type .html text/html"
                http_response = ("<html><body>503 Service Unavailable 503: " + line1[0] + " </body></html>").encode()
                cnt = cntType.split()
                header2 = (cnt[0] + ": " + cnt[2] + "\n")
                self.conn.send(header.encode())
                self.conn.send(header2.encode())
                self.conn.send(b'\n')
                self.conn.send(http_response)
                self.conn.close()

class server_proxy():
    def __init__(self, servaddr, servport, request, conn):
        self.servaddr = servaddr
        self.servport = servport
        self.request = request
        self.conn = conn
        self.check_cache()


    def check_cache(self):
        extn = "cache"
        request2 = self.request.decode()
        request3 = request2.split("\n")
        line1 = request3[0].split()
        homedir = os.getcwd() + "/" + extn
        path = line1[1].split("/")
        n = 3
        filename = homedir + "/" + path[2]
        if os.path.exists(filename):
            k = len(path)
            if k == 3 or path[n] == "":
                extention = "index"
                filename = filename + "/" + extention
            else:
                filename = filename + "/"
                while(n < k):
                    if not path[n] == "":
                        for letter in path[n]:
                            if not letter == "?":
                                filename = filename + letter
                    n = n + 1
        if (os.path.isfile(filename)):
            fh = open(filename, "rb")
            data = fh.read()
            print(data)
            #datadec = data.decode()
            '''for line in datadec:
                print (line)'''
            self.conn.send(data)
        else:
            self.create_socket()

    def create_socket(self):
        try:
            socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socke.connect((self.servaddr, self.servport))    #difference between bind and connect
            print("Server on port " + str(self.servport))
            self.socke = socke
            self.get_data()
            self.socke.close()
        except socket.error as message:
            if socke:
                socke.close()
            print("Could not open socket: " + str(message))
            sys.exit(1)

    def get_data(self):
        flag3 = 0
        flag = 0
        extn = "cache"
        request2 = self.request.decode()
        pathh = os.getcwd()
        filee = pathh + "/" + "private.txt"
        fhh = open(filee, "r")
        dataa = fhh.read()
        dataa2 = dataa.split()
        request3 = request2.split("\n")
        line2 = request3[1].split()
        line22 = line2[1].split(":")
        for linee in dataa2:
            if line22[0] == linee:
                request2 = request2 + "Cache-Control: private"
                flag = 1
                break
            else:
                request2 = request2 + "Cache-Control: public"
        self.request = request2.encode()
        request3 = request2.split("\n")
        line1 = request3[0].split()
        homedir = os.getcwd() + "/" + extn
        path = line1[1].split("/")
        n = 3
        filename = homedir + "/" + path[2]
        if not flag == 1:
            if os.path.exists(filename):
                k = len(path)
                if k == 3 or path[n] == "":
                    extention = "index"
                    filename = filename + "/" + extention
                else:
                    filename = filename + "/"
                    while (n < k):
                        if not path[n] == "":
                            for letter in path[n]:
                                if not letter == "?":
                                    filename = filename + letter
                        n = n + 1
            else:
                os.makedirs(homedir + "/" + path[2])
                k = len(path)
                if k == 3 or path[n] == "":
                    extention = "index"
                    filename = filename + "/" + extention
                else:
                    filename = filename + "/"
                    while (n < k):
                        if not path[n] == "":
                            for letter in path[n]:
                                if not letter == "?":
                                    filename = filename + letter
                        n = n + 1
            print(filename)
        #filename = filename
        self.socke.send(self.request)
        # print(self.request)
        fh = open(filename, "wb")
        while 1:
            data = self.socke.recv(8192)
            #print(data)
            try:
                datadec = data.decode()
                datadec2 = datadec.split()
                for word in datadec2:
                    if word == "pokemon" or word == "Pokemon":
                        header = (line1[2] + " 400 Bad Request\n")
                        cntType = "Content-Type .html text/html"
                        http_response = ("<html><body>400 Bad Request Reason: Cannot be accessed: Contains pokemon </body></html>").encode()
                        flag3 = 1
                        self.conn.send(header.encode())
                        self.conn.send(header2.encode())
                        self.conn.send(b'\n')
                        self.conn.send(http_response)
                        #self.conn.close()
                        break
            except:
                flagg = 0
            if data and not flag3:
                self.conn.send(data)
                if not flag == 1:
                    fh.write(data)
            else:
                break

if __name__ == '__main__':
    global timeout
    if int(sys.argv[1]) < 65535 and int(sys.argv[1]) > 1024:
        port = sys.argv[1]
        proxy = client_Proxy(int(port))
    else:
        print("!")
    try:
        timeout = sys.argv[2]
    except:
        timeout = 100