#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, socket, select


def main():
    if len(sys.argv) != 3:
        print('Illegal options')
        sys.exit(1)

    try:
        host = socket.gethostbyname(sys.argv[1])
    except:
        print("Can't find Host name")
        sys.exit(1)

    # ユーザー名のチェック
    user = sys.argv[2]
    user_char_list = list(user)
    for user_char in user_char_list:
        if not user_char.isalnum() and not ("-" in user_char) and not ("_" in user_char):
            print("Illegal username : %s" % user)
            sys.exit(1)

    port = 10140
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit(1)

    # 参加登録
    while not request_buf:
        request_buf = socket.recv(17).decode()

    if request_buf != "REQUEST ACCEPTED\n":
        sock.close()
        print("Not Accepted")
        sys.exit(1)

    # ユーザ名登録
    sock.send(user)
    while not registered_buf:
        registered_buf = socket.recv(20).decode()

    if registered_buf != "USERNAME REGISTERED\n":
        sock.close()
        print("Not Registered")
        sys.exit(1)
    print("Join as %s" % user)

    while True:
        read_sockets, write_sockets, error_sockets = select.select([sock, ], [sys.stdin, ], [])

        for read_socket in read_sockets:
            if read_socket == sock:
                # 他クライアントからの入力
                receive_buf = socket.recv(1024).decode()
                sys.stdout.write('%s' % receive_buf)

        for write_socket in write_sockets:
            if write_socket == sys.stdin:
                # 標準入力
                msg = sys.stdin.readline().strip()
                if not msg:
                    sock.close()
                    break
                try:
                    sock.send(('%s' % msg).encode())
                except:
                    break


if __name__ == '__main__':
    main()
