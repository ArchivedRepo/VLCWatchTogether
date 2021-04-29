import socket
import threading
import logging
import struct

logging.basicConfig(level=logging.DEBUG)


class Server:

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.clients = []
        self.host_conn = None
        self.host_thread = None

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.listen(5)
        # identity is an unsigned short, 0 for host, 1 for client
        identity_format = '!H'
        identity_size = struct.calcsize(identity_format)
        logging.debug(f'Identity format is {identity_size}')
        while True:
            conn, addr = s.accept()
            logging.info(f'Get connection from {addr}')
            identity = conn.recv(identity_size)
            unpacked = int(struct.unpack(identity_format, identity)[0])
            logging.debug(f'Connection has identity {unpacked}')
            if unpacked == 0:
                if self.host_conn is None:
                    self.host_conn = conn
                    logging.info("Host connected successfully")
                    self.host_thread = threading.Thread(target=self.handle_host, args=())
                    self.host_thread.start()
                else:
                    logging.info("Host already connected, reject this connection")
                    conn.close()
            else:
                logging.info("Client connected successfully")
                self.clients.append(conn)

    def handle_host(self):
        """
        Host command format:
        --------------------
        command - unsigned short
        time - unsigned int
        --------------------
        command list:
        1. pause
        2. play
        3. seek
        """
        command_format = '!HI'
        command_size = struct.calcsize(command_format)
        while True:
            data = self.host_conn.recv(command_size)
            unpacked = struct.unpack(command_format, data)
            this_command, this_time = int(unpacked[0]), int(unpacked[1])
            logging.debug(f'Receive command {this_command}, timestamp {this_time} from host')
            for conn in self.clients:
                conn.sendall(data)


if __name__ == "__main__":
    s = Server('127.0.0.1', 8849)
    s.start_server()
