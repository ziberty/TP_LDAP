from multiprocessing import Process
import time
import ftp.server as FTPfile
import tftp.server
import tftp.client


def server_ftp(args=("epsi", "2022")):
    p = Process(target=FTPfile.server, args=args, name="FTP")
    p.start()
    if p.is_alive():
        print('FTP started')
    else:
        print('error...')
    return p


def client_tftp():
    p = Process(target=tftp.client.init, args=(),name="TFTP client")
    p.start()
    if p.is_alive():
        print('TFTP client started')
    else:
        print('Error...')
    return p

def server_tftp():
    p = Process(target=tftp.server.init, args=(),name="TFTP server")
    p.start()
    if p.is_alive():
        print('TFTP server started')
    else:
        print('Error...')
    return p

if __name__ == '__main__':
    args = ("epsi", "2022")
    ftp = server_ftp(args)

    Choix = input('1:Continue with TFTP \n2:Stop FTP\n Your choice : ')

    if Choix == '2':
        print('FTP server shutdown in progress ...')
        ftp.kill()
        print('FTP server stopped ')
    else:
        print('FTP server shutdown in progress ...')
        ftp.kill()
        print('FTP server stopped ')

        print('Launching the TFTP server process')
        tftp_server = server_tftp()
        time.sleep(5)

        print('Launching the TFTP client process')
        tftp_client = client_tftp()
        time.sleep(5)

#permission read

        if (role == "read" ):
            print('Reading the file')
            file = open('local/pass.data', 'r')
            password = str(file.readline())
            FTPfile.server("epsi", password)
        else:
            print("vous n'avez pas la permision de lecture")