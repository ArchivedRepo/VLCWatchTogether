import logging
import socket
import struct


class Host:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        identity_format = '!H'
        this_identity = struct.pack(identity_format, (0))
        s.sendall(this_identity)
        while True:
            raw_input = input('Command:')
            args = raw_input.split()
            command, time_stamp = int(args[0]), int(args[1])
            command_format = '!HI'
            packed = struct.pack(command_format, command, time_stamp)
            s.sendall(packed)


if __name__ == "__main__":
    Host('127.0.0.1', 8848)