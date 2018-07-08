import socket
import sys
import select

class Client:
    def __init__(self, port, addr):
        self.port       = port
        self.addr       = addr
        self.server     = (None, None)
    
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            self.socket.bind( (self.addr, self.port) )
        except OSError:
            print("Erro ao conectar.")
            sys.exit(1)

    def connect(self, addr, port):
        self.server = addr, port

    def run(self):
        while True:
            readers, _, _ = select.select( [sys.stdin, self.socket], [], [] )

            for reader in readers:
                if reader is self.socket:
                    print(self.socket.recv(1024))
                else:
                    msg = sys.stdin.readline()
                    self.socket.sendto(msg.encode(), self.server)

def main():
    port        = int(sys.argv[1])
    server_ip   = sys.argv[2]
    server_port = int(sys.argv[3])

    client = Client(port, "127.0.0.1")
    client.connect( server_ip, server_port )

    client.run()

if __name__ == '__main__':
    main()