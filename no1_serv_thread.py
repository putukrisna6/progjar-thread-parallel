import zen_utils
from threading import Thread
import sys

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=my_threads, args=t).start()

def my_threads(listener):
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        my_handle_conversation(sock, address)

def my_handle_conversation(sock, address):
    try:
        while True:
            my_handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()

def my_handle_request(sock):
    global value
    value = 0

    len_msg = recvall(sock, 3)
    message = recvall(sock, int(len_msg))
    message = str(message, encoding='ascii')

    m = message.split()
    if m[0] == 'ADD':
        value += int(m[1])
    elif m[0] == 'DEC':
        value -= int(m[1])
    else:
        print('unknown: ', m)
        sys.exit(0)

    msg = str(value)
    len_msg = b'%03d' % (len(msg),)
    msg = len_msg + bytes(msg, encoding='ascii')
    sock.sendall(msg)
    

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener, 6)