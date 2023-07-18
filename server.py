import socket
import struct
import cv2
import numpy as np
import io
import sys
sys.path.append('./scripts/gradio/')
import depth2img
from PIL import Image

# Import the necessary libraries for image generation using a diffusion model

def start_server():
    host = "0.0.0.0"
    port = 8000  # Make sure this port is not used

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    server.listen(1)
    print("Server started, waiting for clients...")
    while True:
        buff_size = 1024
        client, address = server.accept()
        print(f"Client connected from {address}")
        
        #Receive Prompt data
        prompt_data = client.recv(buff_size).decode()
        print(f"Prompt:[{prompt_data}]")

        #Receive Image data
        img_size = client.recv(4)
        img_size = struct.unpack('!I', img_size)[0]       
        image_data = b""
        while len(image_data) < img_size:
            part = client.recv(buff_size*4)
            if not part:
                break  # the connection is closed
            else:
                image_data += part
        print("-> Received img and prompt data")

        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        save_original_img_path = './original_img_path.jpg'
        cv2.imwrite(save_original_img_path, img)
        print("-> Received image from client!")

        # Generate depth image and new generated image using the diffusion model
        img = Image.fromarray(img)
        result = depth2img.result(img, prompt_data)
        depth_img, gen_img = result[0], result[1]
        depth_np, gen_np = np.array(depth_img), np.array(gen_img)
        print("Image Generated!")

        #Send depth image client
        _, depth_encoded = cv2.imencode('.png', depth_np)
        client.sendall(struct.pack('!i', len(depth_encoded)))  # Send size of depth image
        client.sendall(depth_encoded.tobytes())  # Send depth image
        print("<- Sended depth Image!")
        
        #Send generated image to client
        _, gen_encoded = cv2.imencode('.png', gen_np)
        client.sendall(struct.pack('!i', len(gen_encoded)))  # Send size of new generated image
        client.sendall(gen_encoded.tobytes())  # Send new generated image
        print("<- Sended generated Image!")
        client.close()    
        print("Client is closed.")
        print("------------------------------------------------------------------------------------------")
if __name__ == "__main__":
    start_server()
    