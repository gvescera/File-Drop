# -------------------------------------------------------------
# Name:             client.py
# Purpose:          Client portion of File Drop program.
# Author:           Gregory Vescera
# Last Edited:      7/6/2016
# Python Version:   3.5.1
# -------------------------------------------------------------
import socket
import os
import pygubu
import tkinter as tk, tkinter.filedialog as tkfiledialog, tkinter.messagebox as tkmessagebox

filepath = ''

def main():
	# Creates the socket used to communicate with the server
	s = socket.socket()
	host = socket.gethostname()     # Change to IP address of server machine (e.g., '192.168.1.1')
	port = 12345                    # Can be changed to any open port number on server machine

	# Determines a connection status, later to be displayed on the GUI
	try:
		s.connect((host, port))
		status = 'Connected!'
	except:
		status = 'Not Connected!'

	application(s, status)
	s.send(b'exited')


def application(s, status):
	global filepath
	# GUI setup using pygubu
	root = tk.Tk()
	root.wm_title('File Drop')
	builder = pygubu.Builder()
	builder.add_from_file('client.ui')
	frmMain = builder.get_object('frmMain', root)
	entPath = builder.get_object('entPath')
	entPath['state'] = 'readonly'
	btnOpen = builder.get_object('btnOpen')
	btnDrop = builder.get_object('btnDrop')
	btnRestart = builder.get_object('btnRestart')
	lbTitle = builder.get_object('lbTitle')
	lbTitle['text'] = status
	# Required by pygubu for button clicks to register as function calls
	callbacks = {
		'drop':        lambda: drop(s, filepath),
		'askfilepath': lambda: askfilepath(entPath),
		# 'restart': lambda: restart_program()
	}
	builder.connect_callbacks(callbacks)
	root.mainloop()     # Required by tkinter to display GUI


def drop(s, filepath):
	try:
		# Opens the selected file into a buffer and reads its contents to a string
		f = open(filepath, 'rb')
		lines = f.readlines()
		# Finds the appropriate buffer size, attaches it to the file name and sends it to the server
		nameandbuff = os.path.basename(filepath).replace(' ', '_') + ' ' + str(max([len(line) for line in lines]))
		print(nameandbuff)
		s.send(str(nameandbuff).encode())
		buffconfirm = s.recv(1024).decode()
		print(buffconfirm)
		# Begins loop to send pieces of the file line by line
		for line in lines:
			s.send(line)
			piececonfirm = s.recv(1024).decode()
			print(piececonfirm)
		# Closes the file buffer and tells the server the transfer is done
		f.close()
		s.send('end'.encode())
		s.recv(1024)
	except IOError:
		tkmessagebox.showinfo('Error', 'No such file or directory exists!')


def askfilepath(entPath):
	# Sets the global variable 'filepath' to the selected path
	global filepath
	filepath = tkfiledialog.askopenfilename(title = 'Choose a file...')
	# Updates the entry box with the selected path
	entPath['state'] = 'normal'
	entPath.delete(0, len(entPath.get()))
	entPath.insert(0, filepath)
	entPath['state'] = 'readonly'

# def restart_program():
#     """Restarts the current program.
#     Note: this function does not return. Any cleanup action (like
#     saving data) must be done before calling this function."""
#     python = sys.executable
#     print(sys.argv[0])
#     os.execl(python, 'py ' + sys.argv[0])

if __name__ == '__main__':
	main()

