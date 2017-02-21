#!/usr/bin/env/python3


#
# Network Toolkit v1.0a
# *********************
#
# Created by Kevin M. Thomas 02/21/17.
# CC BY
#
# Python 3.4 application that provides an essential network toolkit with features such as local and remote host identification, IP identification, network services database in addition to a powerful local and remote port scanner that identifies what each network service is associated with it.
#


# Import modules.
import os
import socket
import threading
from queue import Queue

# Set global variable.
global max_port
max_port = 65535

def cls():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

# Menu method.
def menu():
	while True:
		try:
			cls()
			print('Network Toolkit v1.0a')
			print('---------------------')
			print('')
			print('Created by Kevin M. Thomas 04/15/16')
			print('CC BY')
			print('')
			print('Enter 1: Provide Local Machine Host Name')
			print('Enter 2: Provide Local Machine IP Address')
			print('Enter 3: Provide Remote Machine IP Address')
			print('Enter 4: Provide Service Running On A Port')
			print('Enter 5: Provide Machine Open Ports')
			print('Enter 6: Quit')
			menu_select = int(input('\nEnter Selection: '))
			if menu_select == 1:
				provide_local_machine_host_name()
			if menu_select == 2:
				provide_local_machine_ip_address()
			elif menu_select == 3:
				provide_remote_machine_ip_address()
			elif menu_select == 4:
				provide_service_running_on_a_port()
			elif menu_select == 5:
				provide_machine_open_ports()
			elif menu_select == 6:
				break
		except:
			print()

# Obtain local machine method.
def provide_local_machine_host_name():
	cls()
	host_name = socket.gethostname()
	print('Host Name: %s' % host_name)
	input('\nPress any key to continue...')

# Obtain local machine IP address method.
def provide_local_machine_ip_address():
	cls()
	host_name = socket.gethostname()
	ip_address = socket.gethostbyname(host_name)
	print('IP Address: %s' % ip_address)
	input('\nPress any key to continue...')

# Obtain remote machine IP address method.
def provide_remote_machine_ip_address():
	cls()
	while True:
		try:
			remote_host = input('Please enter remote host: ')
			if not remote_host.strip():
				print(' Do not enter blank!')
				continue    
			if len(remote_host) > 20:       
				print(' Please keep the data to less than 20 characters!')
				continue        
		except:
				print(' Please enter valid data!')
				continue     
		else:
			break
	try:
		print('\nIP Address of %s is: %s and is active.' % (remote_host, socket.gethostbyname(remote_host)))
	except socket.error as e:
		print('%s: %s' % (remote_host, e))
	input('\nPress any key to continue...')

# Provide service running on a port method.
def provide_service_running_on_a_port():
	cls()
	while True:
		try:
			port = int(input('Please enter port number: '))
			if port > max_port:       
				print(' There are only 65535 ports!')
				continue 
		except:
			print(' Please enter ONLY numbers!')
			continue
		else:
			break
	try:
		service_name = socket.getservbyport(port)
		print('\nService running on port %s is %s normally.' % (port, service_name))
	except OSError as e:
		print('\nNo such service running on port %s is known.' % port)
	except:
		pass
	input('\nPress any key to continue...')

# Provide open machine ports method.
def provide_machine_open_ports():
	cls()
	while True:
		try:
			target = input('Please enter host [type "localhost" for local computer]: ')
			if not target.strip():
				print(' Do not enter blank!')
				continue    
			if len(target) > 20:       
				print(' Please keep the data to less than 20 characters!')
				continue        
		except ValueError:
				print(' Please enter valid data!')
				continue     
		else:
			break
	print_lock = threading.Lock()
	def port_scanner(port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			con = s.connect((target, port))
			with print_lock:
				try:
					print('\nport', port, 'is open')
					service_name = socket.getservbyport(port)
					print('Service running on port %s is %s normally.' % (port, service_name))
				except OverflowError as e:
					print('There are only 65535 ports.')
				except OSError as e:
					print('No such service running on port %s is known.' % port)
				except:
					pass
			con.close()
		except:
			pass
	def threader():
		while True:
			worker = q.get()
			port_scanner(worker)
			q.task_done()    
	q = Queue()
	for x in range(100):
		t = threading.Thread(target = threader)
		t.daemon = True
		t.start()
	for worker in range(1, max_port):
		q.put(worker)
	try:
		q.join()
	except KeyboardInterrupt:
		print('Process Interrupted!')
	except:
		pass
	input('\nPress any key to continue...')

# Call methods at runtime.
menu()
