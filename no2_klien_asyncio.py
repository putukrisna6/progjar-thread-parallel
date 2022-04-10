import argparse, random, socket, zen_utils
import sys, random, multiprocessing

HOST = "127.0.0.1"
PORT = 1060
NUMJOBS = 6

def worker(address, i, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    # message = b'Gajelas kh '

    # sock.sendall(message)
    # print(zen_utils.recv_until(sock, b'.'))

    message = ''
    for ii in data:
        ii = ii.strip()
        ii += '.'
        msg = bytes(ii, encoding='ascii')

        sock.sendall(msg)

        message = zen_utils.recv_until(sock, b'.')
        message = str(message, encoding='ascii')
        # print('debug', message)

    res = message.split('.')[0]
    print('hasil', i, ':',res)
    sock.close()

if __name__ == '__main__':
    f = open("input.txt")
    data = f.readlines()
    f.close()

    address = (HOST, PORT)
    jobs = []
    for i in range(NUMJOBS):
        p = multiprocessing.Process(target=worker, args=(address, i, data))
        jobs.append(p)
    print("JOBS:", len(jobs))

    for p in jobs:
        p.start()

    for p in jobs:
        p.join()

# vim:sw=4:ai
