'''
THIS MODULE ACTS AS A INODE NUMBER LAYER. NOT ONLY IT SHARES DATA WITH INODE LAYER, BUT ALSO IT CONNECTS TO CLIENT STUB FOR INODE TABLE 
UPDATES. THE INODE TABLE AND INODE NUMBER IS UPDATED IN THE FILE SYSTEM USING THIS LAYER
'''
import InodeLayer, config, MemoryInterface, datetime, InodeOps


#HANDLE OF INODE LAYER
interface = InodeLayer.InodeLayer()

class InodeNumberLayer():

	#ASKS FOR INODE FROM INODE NUMBER FROM MemoryInterface.(BLOCK LAYER HAS NOTHING TO DO WITH INODES SO SEPERTAE HANDLE)
	def INODE_NUMBER_TO_INODE(self, inode_number):
		array_inode = MemoryInterface.inode_number_to_inode(inode_number)
		inode = InodeOps.InodeOperations().convert_array_to_table(array_inode)
		if inode: inode.time_accessed = datetime.datetime.now()   #TIME OF ACCESS
		return inode

	#RETURNS DATA BLOCK FROM INODE NUMBER
	def INODE_NUMBER_TO_BLOCK(self, inode_number, offset, length):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if not inode:
			print("Error InodeNumberLayer: Wrong Inode Number! \n")
			return -1
		return interface.read(inode, offset, length)


	#UPDATES THE INODE TO THE INODE TABLE
	def update_inode_table(self, table_inode, inode_number):
		if table_inode: table_inode.time_modified = datetime.datetime.now()  #TIME OF MODIFICATION 
		array_inode = InodeOps.InodeOperations().convert_table_to_array(table_inode)
		MemoryInterface.update_inode_table(array_inode, inode_number)


	#FINDS NEW INODE INODE NUMBER FROM FILESYSTEM
	def new_inode_number(self, type, parent_inode_number, name):
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			max_entries = (config.INODE_SIZE - 79 ) / entry_size
			if len(parent_inode.directory) == max_entries:
				print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
				return -1
		for i in range(0, config.MAX_NUM_INODES):
			if self.INODE_NUMBER_TO_INODE(i) == False: #FALSE INDICTES UNOCCUPIED INODE ENTRY HENCE, FREE INODE NUMBER
				inode = interface.new_inode(type)
				inode.name = name
				self.update_inode_table(inode, i)
				return i
		print("Error InodeNumberLayer: All inode Numbers are occupied!\n")


	#REMOVES THE INODE ENTRY FROM INODE TABLE
	def remove_inode_number(self, inode_number, parent_inode_number):

		def delete_dir(inode_number, parent_inode_number):
			inode = self.INODE_NUMBER_TO_INODE(inode_number)
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if inode.name not in parent_inode.directory: 
				print("InodeNumberLayer: No Such directory")
				return -1
			del parent_inode.directory[inode.name]
			self.update_inode_table(False, inode_number)
			self.update_inode_table(parent_inode, parent_inode_number)

		def delete_file(inode_number, parent_inode_number):
			file_inode = self.INODE_NUMBER_TO_INODE(inode_number)  
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if file_inode.name not in parent_inode.directory: 
				print("InodeNumberLayer: No Such file")
				return -1
			if file_inode.links > 1:   #if hardlink exists
				print("InodeNumberLayer: Hardlink exists")
				file_inode.links -= 1  
				self.update_inode_table(file_inode, inode_number)  #update file_inode 
			else:
				interface.free_invalid_data_block(file_inode, 0)  #free locks if no other hardlink
				self.update_inode_table(False, inode_number)      #free inode
			del parent_inode.directory[file_inode.name]           #delete from parent dir
			self.update_inode_table(parent_inode, parent_inode_number)  #update parent

		def recurse(inode_number, parent_inode_number):
			inode = self.INODE_NUMBER_TO_INODE(inode_number)
			if inode.type == 0: 
				delete_file(inode_number, parent_inode_number)
				return
			for x in list(inode.directory):
				#if x != "." and x != "..":
				recurse(inode.directory[x], inode_number)
			delete_dir(inode_number, parent_inode_number)

		recurse(inode_number, parent_inode_number)


	#IMPLEMENTS WRITE FUNCTIONALITY
	def write(self, inode_number, offset, data, parent_inode_number, filename):
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		if not parent_inode:
			print("Error InodeNumberLayer: No such file\n")
			return -1
		if filename not in parent_inode.directory:
			print("Error InodeNumberLayer: No Such file\n")
			return -1
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		updated_inode = interface.write(inode, offset, data)
		self.update_inode_table(updated_inode, inode_number)


	#IMPLEMENTS READ FUNCTIONALITY
	def read(self, inode_number, offset, length, parent_inode_number, filename):
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		if not parent_inode:
			print("Error InodeNumberLayer: No such file\n")
			return -1
		if filename not in parent_inode.directory:
			print("Error InodeNumberLayer: No Such file!\n")
			return -1
		updated_inode, data = self.INODE_NUMBER_TO_BLOCK(inode_number, offset, length)
		self.update_inode_table(updated_inode, inode_number)
		return data

	#IMPLEMENTS RENAME
	def rename(self, old_name, new_name, parent_inode_number):
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		if new_name in parent_inode.directory:
			print("Error InodeNumberLayer: File with same name already exists!\n")
			return -1
		child_inode_number = parent_inode.directory[old_name]
		child_inode = self.INODE_NUMBER_TO_INODE(child_inode_number)
		child_inode.name = new_name
		del parent_inode.directory[old_name]
		parent_inode.directory[new_name] = child_inode_number 
		self.update_inode_table(child_inode, child_inode_number)
		self.update_inode_table(parent_inode, parent_inode_number)


	def link(self, filename, file_inode_number, hardlink_name, file_parent_inode_number, hardlink_parent_inode_number):
		file_inode = self.INODE_NUMBER_TO_INODE(file_inode_number)
		if file_inode.type == 1: 
			print("Error InodeNumberLayer: Hardlinks of directory not allowed!\n")
			return -1
		hardlink_parent_inode = self.INODE_NUMBER_TO_INODE(hardlink_parent_inode_number)
		if hardlink_name in hardlink_parent_inode.directory:
			print("Error InodeNumberLayer: File already exist in directory. Can not make hardlink with same name!\n")
			return -1
		hardlink_parent_inode.directory[hardlink_name] = file_inode_number
		file_inode.links += 1
		self.update_inode_table(file_inode, file_inode_number)
		self.update_inode_table(hardlink_parent_inode, hardlink_parent_inode_number)


	def mv(self, name, inode_number, old_parent_inode_number, new_parent_inode_number):
		old_parent_inode = self.INODE_NUMBER_TO_INODE(old_parent_inode_number)
		new_parent_inode = self.INODE_NUMBER_TO_INODE(new_parent_inode_number)
		if name in new_parent_inode.directory:
			print("Error InodeNumberLayer: Cannot move file. File already exists!\n")
			return -1
		new_parent_inode.directory[name] = inode_number
		del old_parent_inode.directory[name]
		self.update_inode_table(old_parent_inode, old_parent_inode_number)
		self.update_inode_table(new_parent_inode, new_parent_inode_number)