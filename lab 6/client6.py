import socket
import sys


class Client:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def register(self, client_id):
        msg = 'id_' + client_id
        self.socket.send(msg.encode())

    def send_transaction(self, msg):
        self.socket.send(msg.encode())
        response = self.socket.recv(1024).decode()
        return response

    def close(self):
        self.socket.send('5'.encode())
        self.socket.close()


def main():
    client = Client()
    client_id = input(
        "Enter your first name and ID (Ex: John123): ").replace(' ', '')
    client.register(client_id)

    while True:
        print("\nEnter the number according to the option you want:")
        print("1: Withdraw\n2: Deposit\n3: Transfer\n4: Balance\n5: Exit")
        option = input("Your choice: ")

        if option == '1':
            amount = input("Enter the amount to withdraw: ")
            msg = option + client_id + '.' + amount
            response = client.send_transaction(msg)
            print("Transaction Successful!" if response ==
                  '1' else "Insufficient funds.")

        elif option == '2':
            amount = input("Enter the amount to deposit: ")
            msg = option + client_id + '.' + amount
            response = client.send_transaction(msg)
            print("Deposit Successful!" if response ==
                  '1' else "Deposit Failed.")

        elif option == '3':
            recipient = input("Enter the recipient's ID: ")
            amount = input("Enter the amount to transfer: ")
            msg = option + client_id + '.' + recipient + '.' + amount
            response = client.send_transaction(msg)
            if response == '2':
                print("Transfer Successful!")
            elif response == '1':
                print("Invalid recipient.")
            else:
                print("Insufficient funds.")

        elif option == '4':
            msg = option + client_id
            balance = client.send_transaction(msg)
            print("Your balance is:", balance)

        elif option == '5':
            client.close()
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
