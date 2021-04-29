import logging
import socket
import struct
import VLCController as vlc
logging.basicConfig(level=logging.INFO)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.controller = vlc.VLCController('http://localhost:8080', 1234)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        identity_format = '!H'
        this_identity = struct.pack(identity_format, (1))
        s.sendall(this_identity)

        while True:
            command_format = '!HI'
            command_size = struct.calcsize(command_format)
            data = s.recv(command_size)
            unpacked = struct.unpack(command_format, data)
            this_command, this_time = int(unpacked[0]), int(unpacked[1])
            logging.info(f"Receive command {this_command} with time stamp {this_time}")
            if this_command == 1:
                self.controller.pause()
            elif this_command == 2:
                self.controller.play()
            elif this_command == 3:
                self.controller.seek(this_time)
            else:
                logging.error(f"Logic Fault: unrecognized command {this_command}")


if __name__ == "__main__":
    Client('127.0.0.1', 8848)