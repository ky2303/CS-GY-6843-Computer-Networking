from socket import *
debug = False

def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port))
    # Fill in end

    recv = clientSocket.recv(1024).decode()
    if debug:
        print(recv)
        if recv[:3] != '220': print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    if debug:
        print('1: ' + recv1)
        if recv1[:3] != '250':
            print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    # Fill in start
    mailfromCommand = 'MAIL FROM:<bob@example.org>\r\n'
    clientSocket.send(mailfromCommand.encode())
    recv2 = clientSocket.recv(1024).decode()
    if debug:
        print('2: ' + recv2)
    # Fill in end

    # Send RCPT TO command and print server response.
    # Fill in start
    rcpttoCommand = 'RCPT TO:<alice@example.com>\r\n'
    clientSocket.send(rcpttoCommand.encode())
    recv3 = clientSocket.recv(1024).decode()
    if debug:
        print('3: ' + recv3)
    # Fill in end

    # Send DATA command and print server response.
    # Fill in start
    dataCommand = 'DATA\r\n'
    clientSocket.send(dataCommand.encode())
    recv4 = clientSocket.recv(1024).decode()
    if debug:
        print('4: ' + recv4)
    # Fill in end

    # Send message data.
    # Fill in start
    messagedataCommand = 'Hello Alice\r\n\r\n.\r\n'
    clientSocket.send(messagedataCommand.encode())
    recv5 = clientSocket.recv(1024).decode()
    if debug:
        print('5: ' + recv5)
    # Fill in end

    # Send QUIT command and get server response.
    # Fill in start
    quitCommand = 'QUIT\r\n'
    clientSocket.send(quitCommand.encode())
    recv6 = clientSocket.recv(1024).decode()
    if debug:
        print('6: ' + recv6)
    # Fill in end


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
