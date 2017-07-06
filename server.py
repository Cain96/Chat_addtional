#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, socket, select


def broadcast(socklist, userdict, server_socket, sock, msg):
    # 配信処理
    for socket in socklist:
        if socket != server_socket and socket != sock:
            user = userdict[sock]
            try:
                msg = user + ">" + msg
                socket.send(msg.encode())
            except:
                socket.close()
                userdict.pop(sock)
                socklist.remove(socket)


def server():
    if len(sys.argv) != 1:
        print('Illegal options')
        sys.exit(1)

    port, socklist, host, userdict = 10140, [], "", {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    socklist.append(server_socket)

    while True:
        try:
            read_sockets, write_sockets, error_sockets = select.select(socklist, [], [])
            for sock in read_sockets:
                if sock == server_socket:

                    # 参加受付
                    new_sock, addr = server_socket.accept()
                    if len(socklist) < 5:
                        new_sock.send(("REQUEST ACCEPTED\n").encode())
                        print("REQUEST ACCEPTED")
                        socklist.append(new_sock)
                    else:
                        new_sock.send(("REQUEST REJECTED\n").encode())
                        print("REQUEST REJECTED")
                        new_sock.close()
                        break

                    # ユーザ名登録
                    user = ""
                    while not user:
                        user = new_sock.recv(1024).decode()
                    user = (user.split("\n"))[0]
                    if user in userdict.values():
                        new_sock.send(("USERNAME REJECTED\n").encode())
                        print("USERNAME REJECTED")
                        socklist.remove(new_sock)
                        new_sock.close()
                        break
                    new_sock.send(("USERNAME REGISTERED\n").encode())
                    print("USERNAME REGISTERED")
                    print("Join User : %s" % user)
                    userdict.update({new_sock: user})
                    broadcast(socklist, userdict, server_socket, new_sock, 'User Join\n')

                else:
                    try:
                        msg = sock.recv(1024).decode()
                        if not msg:
                            raise Exception
                        else:
                            broadcast(socklist, userdict, server_socket, sock, msg)
                    except Exception as e:
                        # 離脱処理
                        print('[%s] Exit' % userdict[sock])
                        broadcast(socklist, userdict, server_socket, sock, '[%s] Exit\n' % userdict[sock])
                        userdict.pop(sock)
                        sock.close()
                        socklist.remove(sock)
        except KeyboardInterrupt:
            for sock in socklist:
                sock.close()
            sys.exit()


if __name__ == '__main__':
    server()
