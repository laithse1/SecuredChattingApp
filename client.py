# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import DES_Decrypt
import DES_Encrypt
import el_gamal_Algo
import RSA

HOST = '192.168.56.1'  # Change the host to your machine's IP address
PORT = 3001  # This can be changed to your preferred port


LIME_GREEN= 'lime green'
Light_Yellow2 = 'LightYellow2'
GREEN = 'green'


WHITE = "white"
FONT = ("Ubuntu Medium", 18)
BUTTON_FONT = ("Ubuntu Medium", 16)
SMALL_FONT = ("Ubuntu Medium", 14)

# Creating a socket object
# AF_INET: The server implementation is using IPv4 addresses
# SOCK_STREAM: The server implementation is using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to the server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to the server", f"Unable to connect to the server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        print("SEND : ", username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    # tk
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    username_button.pack_forget()
    username_textbox.pack_forget()
    username_label['text'] = "Welcome " + username + " to our secured Chatting App, Enjoy!"



####here
def send_message():
    message = message_textbox.get()
    if message != '':
        message_textbox.delete(0, len(message))

        # encryption
        if flagMethod == 1:
            message = DES_Encrypt.startDesEncryption(message, key)
        elif flagMethod == 2:
            print("elgamal encryption")
            global messageCopy
            message = el_gamal_Algo.incrypt_gamal(int(elgamalkey[0]), int(elgamalkey[1]), int(elgamalkey[2]), message)

            print("message text= ", message)
            # {q, a, YA, XA}

            messageCopy = message

            # cipher after encryption in var message
        elif flagMethod == 3:
            print("RSA encryption")
            global vo
            pla = []
            global mes
            mes = []
            pla, mes = RSA.preprocess_message(message, int(rsa_string[0]))
            print("mes:", mes)
            message = RSA.to_cipher(int(rsa_string[1]), int(rsa_string[0]), pla)
            message = [str(x) for x in message]
            message = ",".join(message)
            print("msg type:", type(message))
            print("cipher RSA : ", message)

        client.sendall(message.encode("utf-8"))
        print("SEND : ", message.encode())

        print("This message has been delivered")
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


####here
def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        print("RECV : ", message)
        #####
        if message != '':
            message = message.split("~")
            global key, flagMethod, elgamalkey, rsa_string

            username = message[0]
            content = message[1]
            key = message[2]
            flagMethod = int(message[3])
            elgamalkey = message[4]
            elgamalkey = elgamalkey.split(",")
            # print("test:" + elgamalkey[0] + elgamalkey[1] + elgamalkey[2])
            rsa_string = message[5]
            rsa_string = rsa_string.split(",")

            print(elgamalkey)
            print("Client Public Key is:",key)
            print("System flag is: ", flagMethod)

            # decrypt
            if username != "SERVER":
                if flagMethod == 1:

                    content = DES_Decrypt.startDesDecryption(content, key)
                    try:
                        content = bytes.fromhex(content).decode('utf-8')
                    except:
                        print("error")



                elif flagMethod == 2:
                    print("elgamal decryption")
                    print("content copy message=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==- ", content)
                    content = el_gamal_Algo.decrept_gamal(content, int(elgamalkey[3]))




                elif flagMethod == 3:
                    # print("RSA decryption")
                    # print("rsa_string 2 :", int(rsa_string[2]))
                    # print("rsa_string 0 :",int(rsa_string[0]))
                    # print("content",content)
                    # print("mes",mes)

                    content = content.split(",")
                    content = [int(x) for x in content]

                    content = RSA.to_plain(int(rsa_string[2]), int(rsa_string[0]), content, mes)
                    print("RSA Done:", content)

            #
            add_message(f"[{username}] {content}")

        else:
            messagebox.showerror("Error!!", "The Message that was entered by the user is empty")


def DES_Encryption(pt, key):
    cipher = DES_Encrypt.startDesEncryption(pt, key)
    # print("The Cipher Text: ",cipher)
    return cipher


root = tk.Tk()
root.geometry("626x600")
root.title("Secured ChatApp")
root.resizable(False, True)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=LIME_GREEN)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=Light_Yellow2)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=LIME_GREEN)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter your Name:", font=FONT, bg=LIME_GREEN, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=Light_Yellow2, fg='black', width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg='black', fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=Light_Yellow2, fg='black', width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg='black', fg=WHITE,command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=Light_Yellow2, fg='black', width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


# main function
def main():
    # print("CODE :", server.getMethod())
    root.mainloop()


if __name__ == '__main__':
    main()