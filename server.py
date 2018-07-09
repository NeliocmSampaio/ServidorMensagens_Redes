import socket
import sys
import re

class Server:
    def __init__(self, address, port):
        self.tags = {}
        self.address = address
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.socket.bind( (address, port))

    def recv(self):
        return self.socket.recvfrom(1024)

    def insert_tag(self, tag, user):
        if tag not in self.tags:
            self.tags[tag] = []
            #self.tags[tag].append(user)
        if user not in self.tags[tag]:
            self.tags[tag].append(user)

    def remove_tag(self, tag, user):
        if tag not in self.tags:
            return
        else:
            if user in self.tags[tag]:
                self.tags[tag].remove(user)

    def print_table(self):
        #print("type: ", type(self.tags))
        #print(self.tags)
        for i in self.tags:
            print(i)
            for j in self.tags[i]:
                print("\t",j, end='')
            print("")

    def find_tag(self, msg):
        tags = []
        s = msg
        p = s.find('#')

        while p!=-1 and s!='':
            tag = s[p:].split()[0]
            tags.append(tag)
            #print("tag:", tag)
            s = s[p+1:]
            p = s.find('#')

        return tags

    def send_tags(self, msg):
        tags = self.find_tag(msg)
        users = []
        for tag in tags:
            if tag in self.tags:
                for user in self.tags[tag]:
                    if user not in users:
                        self.socket.sendto(msg.encode(), user)
                        users.append(user)

    def add_interest(self, msg, user):
        s = msg
        p = s.find('+')

        while p!=-1 and s!='':
            tag = s[p:].split()[0][1:]
            #print("tag:", tag)
            if tag[0]=='#':
                self.insert_tag(tag, user)
                self.socket.sendto( ("confirmacao de interesse em "+tag+"\n").encode(), user)
            s = s[p+1:]
            p = s.find('+')

    def remove_interest(self, msg, user):
        s = msg
        p = s.find('-')

        while p!=-1 and s!='':
            tag = s[p:].split()[0][1:]
            #print("tag:", tag)
            self.remove_tag(tag, user)
            s = s[p+1:]
            p = s.find('-')

server = Server(sys.argv[1], int(sys.argv[2]) )
while True:
    msg, client = server.recv()
    print(msg.decode(), end='')
    server.add_interest(msg.decode(), client)
    server.remove_interest(msg.decode(), client)
    server.send_tags(msg.decode())
    #server.print_table()