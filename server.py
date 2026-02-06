import socket

UDP_MAX_SIZE = 65535


def listen(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    members = []
    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)

        if addr not in members:
            members.append(addr)

        if not msg:
            continue

        msg_text = msg.decode('ascii')
        client_id = addr[1]
        print(f"recieved: {msg_text}, from: {addr}")
        if msg_text == '__join':
            print(f'Client {client_id} joined chat')
            continue

        message_template = "{}__{}"
        if msg_text == '__members':
            print(f"Client {client_id} requested members list")
            active_members = []
            for member in members:
                print(f"member: {member}")
                if member != addr:
                    active_members.append(f"{member[1]}")
                members_msg = ';'.join(active_members)
                s.sendto(message_template.format("members", members_msg).encode("ascii"), addr)

            continue


        # msg = f'client{client_id}: {msg.decode("ascii")}'
        # for member in members:
        #     if member == addr:
        #         continue
        #
        #     s.sendto(msg.encode('ascii'), member)


if __name__ == '__main__':
    listen()