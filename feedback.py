from ipi_common import *
import os
import os.path

# Subject of feedbackmail
subject = "IPI-Übungsgruppe: Feedback Zettel 2"
# Your name
tutor_name = "Aksel"
# The thunderbird identity from which the mail will be sent
# Apparently, you have to find out the correct identity number
# by trial and error...
sender_id = "id2"

thunderbird_command="thunderbird"

# This script starts thunderbird using the command line arguments as follows
#thunderbird.exe -compose "to='email@domain.com',subject='Some Subject',preselectid='id1',body='Message Body',attachment='File.txt'"

directories = []
with open("directories.txt","r") as directory_file:
  directories = directory_file.read().splitlines()
  
for directory in directories:
  print("Entering " + directory)
  
  message_body = "Hallo,\n\nhier das Feedback zum Zettel:\n\n"
  
  for k,v in tasks.items():
    task_file = os.path.join(directory, "feedback_"+str(k)+".txt")
    message_body += open(task_file, "r").read()
    message_body += "\n\n"
  
  message_body += "\nViele Grüße,\n"+tutor_name
  
  recipients = open(os.path.join(directory,"mail_contact.txt")).read().splitlines()
  recipient_string = ""
  for r in recipients:
    recipient_string += r + ","
  
  compose_arg="subject='"+subject+"',preselectid='"+sender_id+"',to='"+recipient_string+"',"+"body='"+message_body+"'"
  subprocess.call([thunderbird_command,"-compose",compose_arg])
  i=input("Press enter to proceed to next feedback")
