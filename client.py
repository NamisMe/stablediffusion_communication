import socket
import struct
import cv2
import os
import numpy
import base64
import sys

class ClientVideoSocket:
    def __init__(self, ip, port, image_path):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.image_path = image_path
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
            self.sendImages()
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            self.connectServer()

    def sendImages(self, image_path):
        try:
            img = cv2.imread(image_path)
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            _, imgencode = cv2.imencode('.jpg', img, encode_param)
            data = numpy.array(imgencode)
            stringData = base64.b64encode(data)
            length = str(len(stringData))
            self.sock.sendall(length.encode('utf-8').ljust(64))
            self.sock.send(stringData)
        except Exception as e:
            print(e)
            self.sock.close()
            self.connectServer()
            self.sendImages()

def main():
    TCP_IP = 'localhost'
    TCP_PORT = '8000'
    image_path = r'C:\Users\CVLAB\NYJ'
    client = ClientVideoSocket(TCP_IP, TCP_PORT, image_path)

if __name__ == "__main__":
    main()

# def start_client():
#     host="localhost"
#     port=8000

#     sock = socket.socket()
#     sock.connect((host, port))

#     img_path = input("image_path:")
#     img = cv2.imread(img_path)
#     encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
#     result, imgencode = cv2.imencode('.jpg', img, encode_param)
#     data = np.array(imgencode)
#     string
#     stringData = data.tostring()
    
    
    
#     with socket.socket() as sock:
#         sock.connect((host, port))
#         image_path = input("image path: ")
#         image = cv2.imread(image_path)
#         _, imgencode = cv2.imencode('.jpg', image)
#         data = np.array(imgencode)
        
        
#         socket.sendall()


#         prompt = input()
