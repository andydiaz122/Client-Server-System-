import FileSystem

FileSystem.Initialize_My_FileSystem()
interface = FileSystem.FileSystemOperations()


#1. MAKING NEW DIRECTORY
'''
interface.mkdir("/A")
interface.mkdir("/A/B")
interface.mkdir("/A/B/C")
interface.mkdir("D")
interface.status()
'''

#2. WRITING NEW FILES AND READING. [[BEFORE WRTING WE HAVE TO CRTEATE THE FILE ]]
'''
interface.create("/1.txt")
interface.write("/1.txt", "Principles of Computer System Design")
interface.mkdir("/A")
interface.create("/A/2.txt")
interface.write("/A/2.txt", "Hello World!")
interface.status()
interface.read("/1.txt")
interface.read("/A/2.txt", 2, 3)   #reading only 3 words from offset 2 (including the offset)
'''

#3. OVERWIRING OR APPEND FILE AT THE GIVEN OFFSET.
'''
interface.create("/1.txt")
interface.write("/1.txt", "ABC")
interface.read("/1.txt")
interface.write("/1.txt", "D", 1)
interface.status()
interface.read("/1.txt", 0, 1)
'''

#4. DELETING AND REMOVING DIRECTORIES
'''
interface.create("/1.txt")
interface.write("/1.txt", "Principles of Computer System Design")
interface.status()   #in status the file 1.txt is present and data blocks are occupied.
interface.rm("/1.txt")
interface.status()   #now it is deleted from the root and data blocks are also free.
'''


#5. HIERARCHICAL DELETE
#Initializing files and directories in this way, such as '/'' includes 'A' and so on. 
#Now if we delete B directory, all the directories below B directory should be deleted and blocks of all files below B shoud be freed.
#All the files and directories of internal directory should  also be deleted and so on.... till every thing is not deleted.(including B). 
#This is implemented using RECURSION, whihch shows the hierarchy of the file system.
#/ : A   
#A : B
#B : C, D, 3.txt
#C : 1.txt
#D : 2.txt
'''
interface.mkdir("/A")
interface.mkdir("/A/B")
interface.mkdir("/A/B/C")
interface.create("/A/B/C/1.txt")
interface.write("/A/B/C/1.txt", "Principles of Computer System Design")
interface.mkdir("/A/B/D")
interface.create("/A/B/D/2.txt")
interface.write("/A/B/D/2.txt", "University of Florida")
interface.create("/A/B/3.txt")
interface.write("/A/B/3.txt", "Hello!")
interface.status()   #we can see in the status of file system before calling remove B
interface.rm("/A/B")
interface.status()   #After removing B, we have only root and A directory. Moreover, the blocks are also freed.
'''


#6. RENAME
#Renaming a directory and a file.
#A(dir) => B(dir)
#POCSD.txt(file) => CENTRA.txt(file)

'''
interface.mkdir("/A")
interface.create("/POC.txt")
interface.write("/POC.txt", "Principles of Computer System Design")
interface.status()  #Earlier in status POCSD and A is there 
interface.rename("/A", "B")
interface.rename("/POC.txt", "CEN.txt")   
interface.status()  #Now after renaming CENTRA nad B is there. Renamed
interface.read("/POC.txt")      #IT gives an error that there is no such file  
interface.read("/CEN.txt")     #It reads the same content of file before renaming
'''


#7. LINK
'''
interface.mkdir("/A")
interface.mkdir("/A/B")
interface.create("/A/B/1.txt")
interface.write("/A/B/1.txt", "Principles of Computer System Design")
interface.status()
interface.link("/A/B/1.txt", "/1.txt")    #making link in the root dir of file present in /A/B
interface.status() 
interface.read("/1.txt")                  #reading the same file
'''


#8. DELETING FILE AFTER CREATING A HARDLINKS
'''
interface.mkdir("/A")
interface.mkdir("/A/B")
interface.create("/A/B/1.txt")
interface.write("/A/B/1.txt", "Principles of Computer System Design")
interface.link("/A/B/1.txt", "/1.txt")
interface.rm("/A/B/1.txt")  #here we can check at the terminal it will say the file will not be deleted as 1 link still exists.
interface.read("/1.txt")    #we can still read the file as 1 link is still there
interface.status()          #we can see in data blcoks that file is still residing in the system
'''




#9. MOVING FILES/DIRECTORIES
'''
interface.mkdir("/A")
interface.mkdir("/A/B")
interface.mkdir("/A/B/C")
interface.create("/A/B/C/1.txt")
interface.write("/A/B/C/1.txt", "Principles of Computer System Design")
interface.create("/A/B/3.txt")
interface.write("/A/B/3.txt", "Hello!")
interface.mv("/A/B", "/")    #we have moved this B directory form 'A' to root
interface.status()          # we can see the status of change
'''




'''*************************SPECICL CASE EXCEPTIONS************************************'''


#1. WHEN TRYING TO CREATE HARDLINK FOR THE DIRECTORY, HARDLINKS OF DIRECTORY NOT ALLOWED
'''
interface.mkdir("/A")
interface.mkdir("/A/B")
interface.link("/A/B", "/C")
'''



#2. WHEN WRONG PATH GIVEN. IT SHOULD INCLUDE / AT THE START EACH PATH
'''
interface.mkdir("a")
'''


#3. WHEN WRITE OFFSET EXCEEDS THE LENGTH OF FILE, THROWS THE ERROR. IT DOES NOT PERFORM WRITE.
'''
interface.create("/1.txt")
interface.write("/1.txt", "hello")
interface.read("/1.txt")
interface.write("/1.txt", "a", 8)
'''


#4. WHEN READ OFFSET EXCEEDS THE LENGTH OF THE FILE, IT WILL THROW ERROR
'''
interface.create("/1.txt")
interface.write("/1.txt", "hello")
interface.read("/1.txt", 100)
'''


#5. WHEN READ LENGTH EXCEEDS THE LENGTH OF THE FILE, IT WILL THROW ERROR
'''
interface.create("/1.txt")
interface.write("/1.txt", "hello")
interface.read("/1.txt", 0, 100000)
'''


#6. WHEN PARENT DIRECTORY DOES NOT EXIST. [[THROWS ERROR]]
'''
interface.create("/A/1.txt")   #(Directory A has not been initialized)
interface.mkdir("/A/B")
'''


#7 WHEN NUMBER OF INODES INCREASED PER SIZE ALLOCATED TO DIRECTORY(SIZE OF TABLE EXCEEDS THE INODE SIZE)  #THROWS ERROR
#In config file max number entries per inode depends upon the
#  a). SIZE OF FILE NAME(CONFIG.MAX_FILE_NAME_SIZE), 
#  b). SIZE OF INODE
#  c). Constant Size of metadata (79)
#  d). Length of inode number(string)
#Therefore the maximum avaialble entries would be 
			#entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			#max_entries = (config.INODE_SIZE - 79 ) / entry_size 
#Thus according the config allows to make only 4 entries in a single folder
'''
interface.mkdir("/A")
interface.mkdir("/B")
interface.mkdir("/C")
interface.mkdir("/D")
'''
#when trying to make 5th directory
'''
interface.mkdir("/A")
interface.mkdir("/B")
interface.mkdir("/C")
interface.mkdir("/D")
interface.mkdir("/E")
'''


#8 WHEN FILE SIZE EXCEEDS THE GIVEN SIZE IN THE INODE
#Remaining space left in file inode = (config.INODE_SIZE - 63 - config.MAX_FILE_NAME_SIZE) / 2)
#Maxi bytes you can write for one txt file (BLOCK_SIZE * (config.INODE_SIZE - 63- config.MAX_FILE_NAME_SIZE) / 2))
#Now according to this config,  max size = 28672
#TEST CASE_1
'''
s = ""
for i in range(28672): s += 'a'
interface.create("/1.txt")
interface.write("/1.txt", s)	 #write happens with no error message.
'''

#TEST CASE_2
'''
s = ""
for i in range(28672+1): s += 'a'
interface.create("/1.txt")
interface.write("/1.txt", s)	 #write happens with error message.
'''