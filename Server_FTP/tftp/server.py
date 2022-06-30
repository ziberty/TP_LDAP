import tftpy

def init(ip='127.0.0.1', port=69):
    print()
    server = tftpy.TftpServer('local/')
    server.listen(ip, port)


if __name__ == '__main__':
    init()
