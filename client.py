import socket
import threading
import random
import os
from config import SERVER_IP

UDP_MAX_SIZE = 65535

commands = ["/connect", "/members", "/add"]

def listen(s: socket.socket, host: str, port: int):
    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)
        msg_port = addr[-1]
        msg = msg.decode("ascii")
        allowed_ports = threading.current_thread().allowed_ports
        if msg_port not in allowed_ports:
            continue
        if not msg:
            continue
        if "__" in msg:
            command, content = msg.split("__")
            if command == "members":
                for n, member in enumerate(content.split(";"), start=1):
                    print('\r\r' + f"{n}: {member}" + "\n" + "you: ", end='')
        else:
            peer_name = f"client{msg_port}"
            print('\r\r' + f"{peer_name}: " + msg + "\n" + "you: ", end='')
        # print('\r\r' + msg.decode('ascii') + '\n' + f'you: ', end='')

def start_listen(target, socket, host, port):
    th = threading.Thread(target=target, args=(socket, host, port), daemon=True)
    th.start()
    return th


def connect(host: str = SERVER_IP, port: int = 3000):
    own_port = random.randint(8000, 9000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.bind((host, own_port))
    s.bind(('0.0.0.0', own_port))
    listen_thread = start_listen(listen, s, host, port)
    allowed_ports = [port]
    listen_thread.allowed_ports = allowed_ports
    sendto = (host, port)

    s.sendto("__join".encode("ascii"), sendto)


    # s.connect((host, port))

    # threading.Thread(target=listen, args=(s,), daemon=True).start()
    #
    # s.send('__join'.encode('ascii'))

    while True:
        msg = input(f'you: ')
        command = msg.split(' ')[0]
        if command in commands:
            if msg == "/members":
                s.sendto("__members".encode("ascii"), sendto)
            if msg == "/add":
                print(sendto)
            if msg.startswith("/connect"):
                peer = msg.split(' ')[-1]
                new_host = msg.split(' ')[-2]
                peer_port = int(peer.replace('client', ''))
                allowed_ports.append(peer_port)
                sendto = (new_host, peer_port)
                print(f"Connect to {peer_port}")
        else:
            s.sendto(msg.encode("ascii"), sendto)


        # s.send(msg.encode('ascii'))


if __name__ == '__main__':
    os.system('clear')
    print('Welcome to chat!')
    connect()
