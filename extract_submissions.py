from ipi_common import *
import os
import os.path

content = os.listdir(submission_dir)

matched_directories = []
for directory in content:
  if(is_directory_match(directory)):
    matched_directories.append(directory)
    
for match in matched_directories:
  print("target directory: "+match)

directory_list_file = open('directories.txt', 'w+')  


for match in matched_directories:
  print("Processing "+match)
  filepath, authors = get_author_name(os.path.join(submission_dir,match))
  print("Author detection: "+str(authors))
  author_string = authors[0]+"_"+authors[1]
  
  directory_list_file.write(author_string+"\n")
  if not os.path.exists(author_string):
    os.makedirs(author_string)
  copy(filepath, author_string)
  unpack_archive(filepath, author_string)
  
  for task,subtasks in tasks.items():
    with open(os.path.join(author_string, "feedback_"+task+".txt"),"w+") as feedback_file:
      feedback_file.write("Aufgabe "+str(task)+":\n")
      for st in subtasks:
        feedback_file.write("* Teil "+st+"):\n\n")
      feedback_file.close()
  
  with open(os.path.join(author_string, "mail_contact.txt"),"w+") as contact_file:
    if(len(authors[0]) != 0):
      contact_file.write(name_email_map[authors[0]]+"\n")
    if(len(authors[1]) != 0):
      contact_file.write(name_email_map[authors[1]]+"\n")
    contact_file.close()
  

  
