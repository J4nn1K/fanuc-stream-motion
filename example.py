from src.client import UDPClient

# signal definition
t_max = 8000  # 8 ms time steps (125 Hz)
t = np.linspace(start=0, stop=t_max-1, num=t_max)
signal = 1e-4*t

client = UDPClient("192.168.131.7")
client.connect()

resp = client.send_init_pack()

current_jnt_data = resp[18:27]
print(['%.4f' % jnt for jnt in current_jnt_data])

# iterate through signal
for i, value in enumerate(signal):
  jnt_data = current_jnt_data
  jnt_data[2] += value  # which axis to rotate

  if (i==0): 
    data = [1, 0, 1, jnt_data]  # first command pack
  elif (i < len(signal)-1): 
    data = [resp[2], 0, 1, jnt_data]
  else:
    data = [resp[2], 1, 1, jnt_data]  # last command pack
    
  resp = client.send_command_pack(data)
  
  current_jnt_data = resp[18:27]
  print(['%.4f' % jnt for jnt in current_jnt_data])
  
client.send_end_pack()