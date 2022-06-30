import tftpy


def init(src="tftp/local/pass.dat", dest="pass.data"):
    ip = '127.0.0.1'
    port = 69
    client = tftpy.TftpClient(ip, port)
    try:
#permission upload

        if (role == "upload"):
            client.upload(input=src, filename=dest)
        else:
            raise Exception("vous ne possedez pas la permission d'upload")
    except:
        print(Exception.message)

if __name__ == '__main__':
    init("local/pass.dat", "pass.data")
