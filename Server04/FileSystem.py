import MemoryInterface, AbsolutePathNameLayer, pickle

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0):
        interface.write(path, offset, data)
      

    #READ
    def read(self, path, offset=0, size=-1):
        read_buffer = interface.read(path, offset, size)
        if read_buffer != -1:
            print(path + " : " + read_buffer)
            serial_data = pickle.dumps(read_buffer)
            return serial_data
    
    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #RENAME
    def rename(self, old_path, new_name):
        interface.rename(old_path, new_name)
    

    #LINK
    def link(self, old_path, new_path):
        interface.link(old_path, new_path)

    #UN-LINK
    def unlink(self, path):
        interface.unlink(path)

    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)


    #CHECK STATUS
    def status(self):
        MemoryInterface.status()


