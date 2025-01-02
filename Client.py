" This is the Client / Interactive Window"

import sys, xmlrpc.client, pickle, time

print("There are 4 servers available to run")


starting_port_num = input("Please give a 4-digit port number and press enter to start servers:\n")	
server_1_port_num = int(starting_port_num)
server_2_port_num = server_1_port_num + 1
server_3_port_num = server_1_port_num + 2
server_4_port_num = server_1_port_num + 3

server1_http = 'http://localhost:'+ str(server_1_port_num)
server2_http = 'http://localhost:'+ str(server_2_port_num)
server3_http = 'http://localhost:'+ str(server_3_port_num)
server4_http = 'http://localhost:'+ str(server_4_port_num)

server1 = xmlrpc.client.ServerProxy(server1_http)
print("connection established from server01.py")

server2 = xmlrpc.client.ServerProxy(server2_http)
print("connection established from server02.py")

server3 = xmlrpc.client.ServerProxy(server3_http)
print("connection established from server03.py")

server4 = xmlrpc.client.ServerProxy(server4_http)
print("connection established from server04.py")
print(server1.system.listMethods())

server1_not_avail_flag = 0
server2_not_avail_flag = 0
server3_not_avail_flag = 0
server4_not_avail_flag = 0

path_or_file_dict = {}

# write_tracker balances the writes between [server01,server02] and [server03,server04]
write_tracker = 0;
tracker = 0
sub_tracker_1_2 = 0
sub_tracker_3_4 = 0


while 1:
	"Take in command from user and map to corresponding RPCs"
	command_and_argument_string = input("$ ")
	command_and_argument_string = str.split(command_and_argument_string)
	command = command_and_argument_string[0]
	
	# Find out which servers are available
	if server1_not_avail_flag == 0:
		try:
			server1.check_server()
		except:
			print("Connection lost to server01.py")
			server1_not_avail_flag = 1	
	if server2_not_avail_flag == 0:
		try:
			server2.check_server()
		except:
			print("Connection lost to server02.py")
			server2_not_avail_flag = 1	
	if server3_not_avail_flag == 0:
		try:
			server3.check_server()
		except:
			print("Connection lost to server03.py")
			server3_not_avail_flag = 1	
	if server4_not_avail_flag == 0:
		try:
			server4.check_server()
		except:
			print("Connection lost to server04.py")
			server4_not_avail_flag = 1	

		
	try: 
		
		if command == "status":
			if server1_not_avail_flag == 0:
				server1.status()
			if server2_not_avail_flag == 0:
				server2.status()
			if server3_not_avail_flag == 0:
				server3.status()
			if server4_not_avail_flag == 0:
				server4.status()
		elif command == "exit":
			sys.exit()
		else:
			# The following commands make changes to the server filesystems
			# (COMPLETED)
			if command == "create":
				# if write_tracker = 0 then write to [server01,server02]
				try:
					if write_tracker == 0:
						if sub_tracker_1_2 == 0:
							if server1_not_avail_flag == 0:
								server1.create(command_and_argument_string[1])
							if server2_not_avail_flag == 0:
								server2.create(command_and_argument_string[1])
							sub_tracker_1_2 = 1
						elif sub_tracker_1_2 == 1:
							if server2_not_avail_flag == 0:
								server2.create(command_and_argument_string[1])
							if server1_not_avail_flag == 0:
								server1.create(command_and_argument_string[1])
							sub_tracker_1_2 = 0
						write_tracker = 1	
				except:
					if sub_tracker_3_4 == 0:
						if server3_not_avail_flag == 0:
							server3.create(command_and_argument_string[1])
						if server4_not_avail_flag == 0:
							server4.create(command_and_argument_string[1])	
						sub_tracker_3_4 = 1
					elif sub_tracker_3_4 == 1:
						if server4_not_avail_flag == 0:
							server4.create(command_and_argument_string[1])
						if server3_not_avail_flag == 0:
							server3.create(command_and_argument_string[1])	
						sub_tracker_3_4 = 0			
					# else write to server [server03,server04]
				try:
					if write_tracker == 1:	
						if sub_tracker_3_4 == 0:
							if server3_not_avail_flag == 0:
								server3.create(command_and_argument_string[1])
							if server4_not_avail_flag == 0:
								server4.create(command_and_argument_string[1])
							sub_tracker_3_4 = 1
						elif sub_tracker_3_4 == 1:
							if server4_not_avail_flag == 0:
								server4.create(command_and_argument_string[1])
							if server3_not_avail_flag == 0:
								server3.create(command_and_argument_string[1])
							sub_tracker_3_4 = 0		
						write_tracker = 0									
				except:	
					if sub_tracker_1_2 == 0:
						if server1_not_avail_flag == 0:
							server1.create(command_and_argument_string[1])
						if server2_not_avail_flag == 0:
							server2.create(command_and_argument_string[1])
						sub_tracker_1_2 = 1
					elif sub_tracker_1_2 == 1:
						if server2_not_avail_flag == 0:
							server2.create(command_and_argument_string[1])
						if server1_not_avail_flag == 0:
							server1.create(command_and_argument_string[1])
						sub_tracker_1_2 = 0									
			# (COMPLETED)
			elif command == "mkdir":
				# if write_tracker = 0 then write to [server01,server02]
				try:
					if write_tracker == 0:
						if sub_tracker_1_2 == 0:
							if server1_not_avail_flag == 0:
								server1.mkdir(command_and_argument_string[1])
							if server2_not_avail_flag == 0:
								server2.mkdir(command_and_argument_string[1])
							sub_tracker_1_2 = 1
						elif sub_tracker_1_2 == 1:
							if server2_not_avail_flag == 0:
								server2.mkdir(command_and_argument_string[1])
							if server1_not_avail_flag == 0:
								server1.mkdir(command_and_argument_string[1])
							sub_tracker_1_2 = 0			
						write_tracker = 1			
					elif write_tracker == 1:
						if sub_tracker_3_4 == 0:
							if server3_not_avail_flag == 0:
								server3.mkdir(command_and_argument_string[1])
							if server4_not_avail_flag == 0:
								server4.mkdir(command_and_argument_string[1])
							sub_tracker_3_4 = 1
						elif sub_tracker_3_4 == 1:
							if server4_not_avail_flag == 0:
								server4.mkdir(command_and_argument_string[1])
							if server3_not_avail_flag == 0:
								server3.mkdir(command_and_argument_string[1])
							sub_tracker_3_4 = 0		
						write_tracker = 0						
				# else write to server [server03,server04]
				except:
					if write_tracker == 0:
						if sub_tracker_3_4 == 0:	
							if server3_not_avail_flag == 0:
								server3.mkdir(command_and_argument_string[1])
							if server4_not_avail_flag == 0:
								server4.mkdir(command_and_argument_string[1])
							sub_tracker_3_4 = 1
						elif sub_tracker_3_4 == 1:
							if server4_not_avail_flag == 0:
								server4.mkdir(command_and_argument_string[1])
							if server3_not_avail_flag == 0:
								server3.mkdir(command_and_argument_string[1])
							sub_tracker_3_4 = 0
					elif write_tracker == 1:
						if sub_tracker_1_2 == 0:
							if server1_not_avail_flag == 0:
								server1.mkdir(command_and_argument_string[1])
							if server2_not_avail_flag == 0:
								server2.mkdir(command_and_argument_string[1])		
							sub_tracker_1_2 = 1
						elif sub_tracker_1_2 == 1:
							if server2_not_avail_flag == 0:
								server2.mkdir(command_and_argument_string[1])
							if server1_not_avail_flag == 0:
								server1.mkdir(command_and_argument_string[1])			
							sub_tracker_1_2 = 0					
			elif command == "mv":
				old_path = command_and_argument_string[1]
				new_path = command_and_argument_string[2]
				# Try [server1, server2] ... if error occurs do server pairs [server3, server4] 
				try:
					if sub_tracker_1_2 == 0:
						if server1_not_avail_flag == 0:
							server1.mv(old_path, new_path)
						if server2_not_avail_flag == 0:
							server2.mv(old_path, new_path)
						sub_tracker_1_2 = 1
					elif sub_tracker_1_2 == 1:
						if server2_not_avail_flag == 0:
							server2.mv(old_path, new_path)
						if server1_not_avail_flag == 0:
							server1.mv(old_path, new_path)
						sub_tracker_1_2 = 0		
				except:
					if sub_tracker_3_4 == 0:
						if server3_not_avail_flag == 0:
							server3.mv(old_path, new_path)
						if server4_not_avail_flag == 0:
							server4.mv(old_path, new_path)
						sub_tracker_3_4 = 1
					elif sub_tracker_3_4 == 1:
						if server4_not_avail_flag == 0:
							server4.mv(old_path, new_path)
						if server3_not_avail_flag == 0:
							server3.mv(old_path, new_path)
						sub_tracker_3_4 = 0
			# (COMPLETED)
			elif command == "write":
				data = command_and_argument_string[2:len(command_and_argument_string)]
				serial_data = pickle.dumps(data)
				try:
					# if write_tracker = 0 then write to [server01,server02]
					if write_tracker == 0:
						if sub_tracker_1_2 == 0:
							if server1_not_avail_flag == 0:
								print("Waiting to write to server01.py ...")
								time.sleep(3)
								server1.write(command_and_argument_string[1], serial_data)
							if server2_not_avail_flag == 0:
								print("Waiting to write in another replica to server02.py ...")
								time.sleep(3)
								server2.write(command_and_argument_string[1], serial_data)
							sub_tracker_1_2 = 1	
						elif sub_tracker_1_2 == 1:
							if server2_not_avail_flag == 0:
								print("Waiting to write to server02.py ...")
								time.sleep(3)
								server2.write(command_and_argument_string[1], serial_data)
							if server1_not_avail_flag == 0:
								print("Waiting to write in another replica to server01.py ...")
								time.sleep(3)
								server1.write(command_and_argument_string[1], serial_data)	
							sub_tracker_1_2 = 0			
						write_tracker = 1								
				# else write to server [server03,server04]
				except:
				#else:
					if sub_tracker_3_4 == 0:
						if server3_not_avail_flag == 0:
							print("Waiting to write to server03.py ...")
							time.sleep(3)
							server3.write(command_and_argument_string[1], serial_data)
						if server4_not_avail_flag == 0:
							print("Waiting to write in another replica to server04.py ...")
							time.sleep(3)
							server4.write(command_and_argument_string[1], serial_data)
						sub_tracker_3_4 = 1
					elif sub_tracker_3_4 == 1:
						if server4_not_avail_flag == 0:
							print("Waiting to write to server04.py ...")
							time.sleep(3)
							server4.write(command_and_argument_string[1], serial_data)
						if server3_not_avail_flag == 0:
							print("Waiting to write in another replica to server03.py ...")
							time.sleep(3)
							server3.write(command_and_argument_string[1], serial_data)
						sub_tracker_3_4 = 0		
				try:
					if write_tracker == 1:
						if sub_tracker_3_4 == 0:
							if server3_not_avail_flag == 0:
								print("Waiting to write to server03.py ...")
								time.sleep(3)
								server3.write(command_and_argument_string[1], serial_data)
							if server4_not_avail_flag == 0:
								print("Waiting to write in another replica to server04.py ...")
								time.sleep(3)
								server4.write(command_and_argument_string[1], serial_data)	
							sub_tracker_3_4 = 1
						elif sub_tracker_3_4 == 1:
							if server4_not_avail_flag == 0:
								print("Waiting to write to server04.py ...")
								time.sleep(3)
								server4.write(command_and_argument_string[1], serial_data)
							if server3_not_avail_flag == 0:
								print("Waiting to write in another replica to server03.py ...")
								time.sleep(3)
								server3.write(command_and_argument_string[1], serial_data)	
							sub_tracker_3_4 = 0			
						write_tracker = 0
				except:
					if sub_tracker_1_2 == 0:
						if server1_not_avail_flag == 0:
							print("Waiting to write to server01.py ...")
							time.sleep(3)
							server1.write(command_and_argument_string[1], serial_data)
						if server2_not_avail_flag == 0:
							print("Waiting to write in another replica to server02.py ...")
							time.sleep(3)
							server2.write(command_and_argument_string[1], serial_data)
						sub_tracker_1_2 = 1
					if sub_tracker_1_2 == 1:
						if server2_not_avail_flag == 0:
							print("Waiting to write to server02.py ...")
							time.sleep(3)
							server2.write(command_and_argument_string[1], serial_data)
						if server1_not_avail_flag == 0:
							print("Waiting to write in another replica to server01.py ...")
							time.sleep(3)
							server1.write(command_and_argument_string[1], serial_data)
						sub_tracker_1_2 = 0									
			# (COMPLETED)
			elif command == "read":
				try:
					if sub_tracker_1_2 == 0:
						if server1_not_avail_flag == 0:
							print("Waiting to read from server01.py")
							time.sleep(3)
							data_read = pickle.loads(server1.read(command_and_argument_string[1]))
						elif server2_not_avail_flag == 0:
							print("Waiting to read from server02.py")
							time.sleep(3)
							data_read = pickle.loads(server2.read(command_and_argument_string[1]))
						sub_tracker_1_2 = 1
					elif sub_tracker_1_2 == 1:
						if server2_not_avail_flag == 0:
							print("Waiting to read from server02.py")
							time.sleep(3)
							data_read = pickle.loads(server2.read(command_and_argument_string[1]))
						elif server1_not_avail_flag == 0:
							print("Waiting to read from server01.py")
							time.sleep(3)
							data_read = pickle.loads(server1.read(command_and_argument_string[1]))
						sub_tracker_1_2 = 0	
				except:
					if sub_tracker_3_4 == 0:
						if server3_not_avail_flag == 0:
							print("Waiting to read from server03.py")
							time.sleep(3)
							data_read = pickle.loads(server3.read(command_and_argument_string[1]))
						elif server4_not_avail_flag == 0:
							print("Waiting to read from server04.py")
							time.sleep(3)
							data_read = pickle.loads(server4.read(command_and_argument_string[1]))
						sub_tracker_3_4 = 1
					elif sub_tracker_3_4 == 1:
						if server4_not_avail_flag == 0:
							print("Waiting to read from server04.py")
							time.sleep(3)
							data_read = pickle.loads(server4.read(command_and_argument_string[1]))
						elif server3_not_avail_flag == 0:
							print("Waiting to read from server03.py")
							time.sleep(3)
							data_read = pickle.loads(server3.read(command_and_argument_string[1]))
						sub_tracker_3_4 = 0	
				print(data_read)
			# (COMPLETED)
			elif command == "rm":
				# Try [server1, server2] ... if error occurs do server pairs [server3, server4] 
				try:
					if sub_tracker_1_2 == 0:
						if server1_not_avail_flag == 0:
							server1.rm(command_and_argument_string[1])
						if server2_not_avail_flag == 0:
							server2.rm(command_and_argument_string[1])
						sub_tracker_1_2 = 1
					elif sub_tracker_1_2 == 1:
						if server2_not_avail_flag == 0:
							server2.rm(command_and_argument_string[1])
						if server1_not_avail_flag == 0:
							server1.rm(command_and_argument_string[1])
						sub_tracker_1_2 = 0		
					write_tracker = 0	
				except:
					if sub_tracker_3_4 == 0:
						if server3_not_avail_flag == 0:
							server3.rm(command_and_argument_string[1])
						if server4_not_avail_flag == 0:
							server4.rm(command_and_argument_string[1])
						sub_tracker_3_4 = 1
					elif sub_tracker_3_4 == 1:
						if server4_not_avail_flag == 0:
							server4.rm(command_and_argument_string[1])
						if server3_not_avail_flag == 0:
							server3.rm(command_and_argument_string[1])
						sub_tracker_3_4 = 0		
					write_tracker = 1
				try:
					if sub_tracker_3_4 == 0:
						if server3_not_avail_flag == 0:
							server3.rm(command_and_argument_string[1])
						if server4_not_avail_flag == 0:
							server4.rm(command_and_argument_string[1])
						sub_tracker_3_4 = 1
					elif sub_tracker_3_4 == 1:
						if server4_not_avail_flag == 0:
							server4.rm(command_and_argument_string[1])
						if server3_not_avail_flag == 0:
							server3.rm(command_and_argument_string[1])
						sub_tracker_3_4 = 0		
					write_tracker = 1
				except:
					if sub_tracker_1_2 == 0:
						if server1_not_avail_flag == 0:
							server1.rm(command_and_argument_string[1])
						if server2_not_avail_flag == 0:
							server2.rm(command_and_argument_string[1])
						sub_tracker_1_2 = 1
					elif sub_tracker_1_2 == 1:
						if server2_not_avail_flag == 0:
							server2.rm(command_and_argument_string[1])
						if server1_not_avail_flag == 0:
							server1.rm(command_and_argument_string[1])
						sub_tracker_1_2 = 0		
					write_tracker = 0				
			else:
				print("Command not recognized")
	except:
		print("Command not used correctly")