# -------------------------------------------------------------
# Name:             server.py
# Purpose:          Server portion of File Drop program.
# Author:           Gregory Vescera
# Last Edited:      7/6/2016
# Python Version:   3.5.1
# -------------------------------------------------------------
import socket


def main():
	session = ''
	# Creates the passive socket
	s = socket.socket()
	host = socket.gethostname()     # Change to IP address of server machine (e.g., '192.168.1.1')
	port = 12345                    # Can be changed to any open port number on server machine
	s.bind((host, port))

	# Waits for and creates client socket when one is detected
	print("Waiting for connection...")
	s.listen(5)
	c, addr = s.accept()
	print(addr, 'has connected.')

	# Enters infinite loop to always be ready to accept new connections
	while True:
		# Beginning of send and receive loop:
		# Receives the name of the file being sent and the maximum buffer size to expect
		nameandbuff = c.recv(1024).decode()
		print(nameandbuff)
		while nameandbuff == 'exited':
			print(nameandbuff)
			s.listen(5)
			c, addr = s.accept()
			print(addr, 'has connected.')
			nameandbuff = c.recv(1024).decode()
		# Separates the filename and buffer size
		filename = (nameandbuff.split())[0]
		buff = int((nameandbuff.split())[1])
		# Opens file buffer to begin copying the data received
		f = open(filename, 'wb')    # Change file name to any directory concatenated with 'filename'
		c.send('Server: Got filename buffsize!'.encode())
		# Enters loop to recreate the file using the data being sent from the client
		while True:
			line = c.recv(buff)
			if line == b'end':  # The loop is broken only if the byte string 'end' is received
				c.send(line)
				break
			f.write(line)
			c.send('Server: Got piece!'.encode())
		f.close()
		# After closing the file buffer, the main loop restarts and the server waits for another connection


if __name__ == '__main__':
	main()
