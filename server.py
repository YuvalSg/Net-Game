import socket
import select

IP = "0.0.0.0"
PORT = 31415

server_socket = socket.socket()
server_socket.bind((IP, PORT))
server_socket.listen(5)

client_sockets = []
messages_to_send = []
client_username_dict = {}


def main():
    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                client_sockets.append(new_socket)
                client_username_dict[new_socket] = None
            else:
                try:
                    data = current_socket.recv(1024)
                except:
                    client_sockets.remove(current_socket)
                else:
                    output = create_output(data, current_socket)
                    messages_to_send.append((current_socket, output))
        send_waiting_messages(wlist)


def send_waiting_messages(wlist):
    '''sends waiting messages that need to be sent, only if client's socket is writeable'''
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(data)
            messages_to_send.remove(message)


def create_output(client_data, current_socket):
    if client_username_dict[current_socket] is None:
        client_username_dict[current_socket] = client_data
        print client_username_dict #debugging
        return "logged in as " + client_data
    return "game information"


if __name__ == "__main__":
    main()


'''character database :
*username
-password
-class (Warrior, Wizard)
-team (White, Red, Monster)
-level
-exp
-max_exp
-hp
-max_hp
-min_damage
-max_damage
'''

'''map_rows database: (Needs better idea how to store maps)
*id : (map_id*1000 + row)
-map_id
-row_id
-columns_data
'''

'''Simple_Client:
import socket
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 31415))
while True:
    my_socket.send(raw_input())
    data = my_socket.recv(1024)
    print data
my_socket.close()
'''