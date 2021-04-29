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
            try:
                command = int(args[0])
                if command != 3:
                    time_stamp = 0
                else:
                    raw_time = args[1]
                    if ':' not in raw_time:
                        time_stamp = int(args[1])
                    else:
                        this_splited = raw_time.split(":")
                        if len(this_splited) == 3:
                            time_stamp = int(this_splited[0]) * 3600 + int(this_splited[1]) * 60 + int(this_splited[2])
                        else:
                            time_stamp = int(this_splited[0]) * 60 + int(this_splited[1])
                command_format = '!HI'
                packed = struct.pack(command_format, command, time_stamp)
                s.sendall(packed)
            except Exception as e:
                logging.error(f"Error in parsing input or sending message, exception {e}")


if __name__ == "__main__":
    Host('127.0.0.1', 8848)