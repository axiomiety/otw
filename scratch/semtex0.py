import socket
HOST = 'semtex.labs.overthewire.org'
PORT = 24000 # x86/elf
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
flag = True
with open('/var/tmp/semtex0.bin','w+') as b:
  while True:
    chunk = s.recv(1)
    if not chunk:
      break
    if flag:
      b.write(chunk)
    flag = False if flag else True
s.close()
