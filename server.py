import socket
import select
import game_player  # QQQQQ

'''
up to do:
1. prevent 2 clients to login to the same player
2. change data stored in objects to databases, marked in QQQQQ
'''

IP = "0.0.0.0"
PORT = 31415
NUMBER_OF_PLAYER_VARS = 2

server_socket = socket.socket()
server_socket.bind((IP, PORT))
server_socket.listen(5)

client_sockets = []
messages_to_send = []
client_username_dict = {}
player_list = []

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
    if client_username_dict[current_socket] is None:  # if client is not logged in
        return registering_and_logging_output(client_data, current_socket)  # do the registering and logging
    return playing_output(client_data, current_socket)  # do the game playing


def registering_and_logging_output(client_data, current_socket):
    client_data = client_data.split("|")

    command = client_data[0]
    client_data = client_data[1:]  # deleting the command from the data

    if command == "r":  # register
        if len(client_data) == NUMBER_OF_PLAYER_VARS:
            player_name = client_data[0]
            password = client_data[1]
            if not name_catched_up(player_name):
                new_player = game_player.game_player(player_name, password)  # QQQQQ
                client_username_dict[current_socket] = new_player  # QQQQQ login
                player_list.append(new_player)  # QQQQQ register
                return "w|logged in as " + player_name
            else:
                return "e|name catched up"
    if command == "l":  # login
        if len(client_data) == 2: #one for username and other for password
            player_name = client_data[0]
            password = client_data[1]
            if name_catched_up(player_name):
                player = search_player(player_name)
                if player.password == password:
                    client_username_dict[current_socket] = player  # QQQQQ login
                    return "w|logged in as " + player_name
                else:
                    return "e|player password is not correct"
            else:
                return "e|player name is not correct"
    else:
        return "e|unknown command"


def name_catched_up(name):
    ''' determines if name is catched up or not '''
    for player in player_list:  # QQQQQ
        if name == player.name:  # QQQQQ
            return True
    return False


def search_player(name):
    for player in player_list:  # QQQQQ
        if name == player.name:  # QQQQQ
            return player
    return None


def playing_output(client_data, current_socket):
    if client_data == "exit":
        client_username_dict[current_socket] = None
        return "logged_out"
    return "inside"


if __name__ == "__main__":
    main()


#short needed codes to run the main code

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


'''timed_class_code:
class game_player:
    def __init__(self, name, password):
        self.name = name
        self.password = password
'''