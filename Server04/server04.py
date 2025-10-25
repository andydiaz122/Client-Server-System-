" This is the Server module"
import FileSystem, pickle
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


	
# Create Server
server = SimpleXMLRPCServer(("localhost", 5003))
server.register_introspection_functions()



" The following functions interface with the file system: "
class MyFuncs:
	def __init__(self):
		FileSystem.Initialize_My_FileSystem()
		self.interface = FileSystem.FileSystemOperations()

	#MAKES NEW DIRECTORYZ
	def mkdir(self, path):
		self.interface.mkdir(path)
		return 1

	#CREATE FILE
	def create(self, path):
		self.interface.create(path)
		return 1

	#MOVING FILE
	def mv(self, old_path, new_path):
	    self.interface.mv(old_path, new_path)	
	    return 1

	#READ
	def read(self, path, offset=0, size=-1):
	    data_read = self.interface.read(path, offset, size)
	    return data_read

	#WRITE TO FILE
	def write(self, path, data, offset=0):
	    self.interface.write(path, data, offset)
	    return 1

	#CHECK STATUS
	def status(self):
	    self.interface.status()
	    return 1

	#DELETE
	def rm(self, path):
	    self.interface.unlink(path)
	    return 1

	def check_server(self):
		return 1

# Register server functions and get server running
#server.register_function(test_func, "test_func")
server.register_instance(MyFuncs())
server.serve_forever()


