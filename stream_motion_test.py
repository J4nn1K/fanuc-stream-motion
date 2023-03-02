from utils import *
from socket import *
import numpy as np
import time
# import tqdm

UDP_IP = "192.168.131.7"
UDP_PORT = 60015

### Signal for motion test ###
t_max = 1000
t = np.linspace(start=0, stop=t_max-1, num=t_max)
signal = 1e-4*np.ones(t_max)

### Clock to monitor communication speed ###
start_time = time.time()

### Connect to socket ###
sock = socket(AF_INET,SOCK_DGRAM)
sock.connect((UDP_IP,UDP_PORT))
print('SOCKET CONNECTED: {:.2f}ms'.format(1000*(time.time()-start_time)))

### Send init pack ###
data = initpack()
sock.sendto(data,(UDP_IP,UDP_PORT))
print('INIT PACK SENT: {:.2f}ms'.format(1000*(time.time()-start_time)))

resp = sock.recv(132)
resp = explainRobData(resp)
# print(resp)

### Extract joint data ###
current_jnt_data = resp[18:27]
print(f'JOINT DATA: {current_jnt_data}')
print('({:.2f}ms)'.format(1000*(time.time()-start_time)))

### Send command packs ###
for i, value in enumerate(signal):
  
  jnt_data = current_jnt_data
  jnt_data[0] += value 

  data = commandpack([1, 0, 1, jnt_data])
  
  sock.sendto(data, (UDP_IP, UDP_PORT))
  
  print('COMMAND PACK SENT:', ['%.2f' % jnt for jnt in jnt_data])
  # print('({:.2f}ms)'.format(1000*(time.time()-start_time)))
  
  resp = sock.recv(132)
  resp = explainRobData(resp) 
  
  current_jnt_data = resp[18:27]
  
### Send end pack ###  
data = endpack()
sock.sendto(data,(UDP_IP,UDP_PORT))
print('END PACK SENT')

sock.close()