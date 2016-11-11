from ipi_common import *
import os
import os.path
import sys

def grade_task(task_num):

  directories = []
  with open("directories.txt","r") as directory_file:
    directories = directory_file.read().splitlines()
  
  for directory in directories:
    task_file = os.path.join(directory, "feedback_"+str(task_num)+".txt")
    print("Entering " + directory)
    print("Accessing " + task_file)
    subprocess.call(["nautilus", directory])
    subprocess.call(["gedit", task_file, "-w"])
    
if(len(sys.argv) == 2):
  grade_task(sys.argv[1])
else:
  print("Invalid number of arguments!")
