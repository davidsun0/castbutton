import socket
import sys
import xinwenquery

#set up server information
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', SERVER PORT) #make sure server is accessible by local network
print >>sys.stderr, 'starting up on port %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)
print 'ready'

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        #connection received
        print >>sys.stderr, 'connection from', client_address
        while True:
            #expecting a length 4 string - xwlb
            data = connection.recv(4)
            print >>sys.stderr, 'received "%s"' % data
            if data == 'xwlb':
                print >>sys.stderr, 'recieved xwlb signal'
                # takes 5 - 6 seconds to send response back to client
                if xinwenquery.play_xwlb():
                    print >>sys.stderr, 'cast sucessful'
		    connection.sendall('200')
                else:
                    print >>sys.stderr, 'cast failed'
                    connection.sendall('501')
                break
            else:
                print >>sys.stderr, 'ending connection', client_address
                break
    finally:
        print >>sys.stderr, 'closing connection'
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
