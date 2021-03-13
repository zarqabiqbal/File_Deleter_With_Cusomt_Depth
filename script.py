#Test 6
import os
import time
from dateutil.parser import parse
import sys

ext_to_delete = ["mp4","py"] #you can choose which extension you want to delete
deleted_file_size = 8 #This data is in MB (Note :- File which is greater than 8mb only deleted)
MAX_DEPTH = 5
file_output = "****************\nDate : {}\nSize : {:.2f} MB\n****************"
success_created = "{} Successfully File Created"
success_deleted = "{} Successfully File Deleted"
error_created = "{} File Making Error"
error_deleted = "{} File Deletion Error"

# function to create file with any string Data
def saveFileWithData(filePath,data):
    try:
    	# open file with write permission
        with open(filePath,'w') as file:
            file.write(data)
            file.close()
            return True
    except:
        return False

#function which accept data in bytes and return data of your desired type (default is KB)
def getFileSize(size_in_byte,return_size='KB'):
    if return_size=="KB":
        return size_in_byte/1024.0
    elif return_size=="MB":
        return size_in_byte/(1024.0*1024.0)
    elif return_size=="GB":
        return size_in_byte/(1024.0*1024.0)

#function to get file list with custom depth
def getFileListWithDepth(root_path,depth):
    if depth:
        try:
            for files in os.listdir(root_path):
#                 join root and files path present in root directory to easy acces
                abs_root_file = os.path.join(root_path,files)
                if os.path.isdir(abs_root_file):
#                     call function itself when any directory found in root directory
                    getFileListWithDepth(abs_root_file,depth-1)
                else:
#                   extract file extension
                    file_path_without_ext,file_ext = os.path.splitext(abs_root_file)
                    if file_ext[1:] in ext_to_delete:
#                         get file stats
                        file_stats = os.stat(abs_root_file)
#                         get file size in MB
                        file_size_in_mb = getFileSize(file_stats.st_size,"MB")
                        if file_size_in_mb > deleted_file_size:
                            new_date = parse(time.ctime(file_stats.st_ctime))
                            if saveFileWithData(file_path_without_ext+".txt",file_output.format(new_date.strftime("%B %m %Y")
                                                                                                ,file_size_in_mb)):
                                print(success_created.format(file_path_without_ext+".txt"))
                                # remove file after txt file created
                                os.remove(abs_root_file)
                                print(success_deleted.format(abs_root_file))
                            else:
                                print(error_created.format(file_path_without_ext+".txt"))
                                print(error_deleted.format(abs_root_file))
                            
        except PermissionError:
            print("Permission Denied for this file or directory {}".format(root_path))
    else:
        return

if __name__ == "__main__":
	arguments = sys.argv
	if len(arguments) < 2:
		print("Please give directory name like this : 'python script.py directory_name'")
		exit(0)
	elif len(arguments) >= 3:
		if arguments[2].isdigit():
			if os.path.isdir(arguments[1]):
				getFileListWithDepth(arguments[1],arguments[1])
			else:
				print(arguments[1],"Directory Not Exist")
		else:
			print("Please give depth size in number : 'python script.py directory_name depth_in_number'")
			exit(0)
	else:
		if os.path.isdir(arguments[1]):
				getFileListWithDepth(arguments[1],MAX_DEPTH)
		else:
			print(arguments[1],"Directory Not Exist")
		