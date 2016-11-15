

import os
import os.path
from shutil import copy
import subprocess
from subprocess import call
import collections

submission_dir = "Alle"
group_member_file = "group_members.txt"

tasks = collections.OrderedDict()
with open('task_description.txt', 'r') as task_description:
  raw_tasks = task_description.readlines()
  for task in raw_tasks:
    t = task.split()
    if(len(t) >= 1):
      subtasks = t[1:]
      tasks[t[0]] = subtasks
  print(tasks)
    

member_lines = []
first_names = []
last_names = []
email_addresses = []
name_email_map = {}


with open(group_member_file) as f:
  member_lines = f.readlines()
 
for member in member_lines:
  s = member.split()
  if(len(s) < 3):
    raise(Exception("Invalid member "+str(member)))
  if(len(s) > 3):
    print("Person with several names detected: "+member+"=> Storing as "+s[0]+" "+s[len(s)-2])
  
  first_name = s[0].lower()  
  last_name = s[len(s)-2].lower()
  email = s[len(s)-1]
  
  first_names.append(first_name)
  last_names.append(last_name)
  email_addresses.append(email)
  name_email_map[first_name+" "+last_name] = email



def sort_by_priority_match(string, first_name_set, last_name_set):
  lower_s = string.lower()
  scores = []
  for first_name, last_name in zip(first_name_set, last_name_set):
    first_name_match = lower_s.find(first_name) != -1
    second_name_match = lower_s.find(last_name) != -1
    score = 0
    if(first_name_match):
      score += 1
    if(second_name_match):
      score += 1
    scores.append((first_name, last_name, score))
  scores.sort(key = lambda s: s[2])
  return scores

def find_highest_priority_match(string, first_name_set, last_name_set):
  scores = sort_by_priority_match(string, first_name_set, last_name_set)
  result = scores[len(scores)-1]
  return result 


def find_two_best_matches(string):
  scores = sort_by_priority_match(string, first_names, last_names)
  name1 = scores[len(scores)-1][0]+" "+scores[len(scores)-1][1]
  name2 = scores[len(scores)-2][0]+" "+scores[len(scores)-2][1]
  next_lowest_score = scores[len(scores)-3][2]
  return (name1, name2, scores[len(scores)-1][2], scores[len(scores)-2][2], next_lowest_score)

def is_directory_match_token(character):
  return character == '_' or character == '-' or character == '-' or character == ' '

def is_directory_match_surrounded_by_tokens(dirname, matchpos, match):
  if(matchpos > 0):
    if(not is_directory_match_token(dirname[matchpos-1])):
      return False
  if(matchpos + len(match) < len(dirname)):
    if(not is_directory_match_token(dirname[matchpos+len(match)])):
      return False
  return True

def is_directory_match(dirname):
  best_match = find_highest_priority_match(dirname, first_names, last_names)
  
  if(best_match[2] == 0):
    return False
  if(best_match[2] == 2):
    return True
  if(best_match[2] == 1):
    print("Possible candidate for "+best_match[0]+" "+best_match[1]+": "+dirname)
    pos_first_name = dirname.lower().find(best_match[0])
    pos_last_name = dirname.lower().find(best_match[1])
    
    
    if(pos_first_name != -1):
      if(is_directory_match_surrounded_by_tokens(dirname, pos_first_name, best_match[0])):
        i = input("Select? [y/N]")
        if(i == 'Y' or i == 'y'):
          return True
        else:
          return False
    elif(pos_last_name != -1):
      if(is_directory_match_surrounded_by_tokens(dirname, pos_last_name, best_match[1])):
        i = input("Select? [y/N]")
        if(i == 'Y' or i == 'y'):
          return True
        else:
          return False
        
  return False 


def get_author_name(target_directory):
  files = os.listdir(target_directory)
  if(len(files) != 1):
    print("Warning: several files are present in target directory: "+target_directory)
    print("  files: "+str(files))
  for filename in files:
    if(filename.lower().find(".zip") != -1 or 
       filename.lower().find(".rar") != -1 or
       filename.lower().find(".7z") != -1 or 
       filename.lower().find(".tar.gz") != -1):
      print("Target file: "+filename)
      filepath = os.path.join(target_directory, filename)
      author_match = find_two_best_matches(filepath)
      authors = ["", ""]
      
      next_lowest_score = author_match[4]
      for i in range(0,2):
        result_score = author_match[2 + i]
        if(result_score <= next_lowest_score):
          print("Author "+str(i+1)+" is uncertain - best guess is: "+author_match[i])
          i = input("Accept (press 'a' to enter alternative)? [a/y/N]")
          if(i == 'y' or i=='Y'):
            authors[0] = author_match[0]
          elif(i == 'a' or i=='A'):
            authors[0] = input("Enter alternative: ")
        else:
          authors[i] = author_match[i]
          
      return (filepath, authors)
    else:
      print("Invalid file type: "+filename)
      return (filepath, ["", ""])


def unpack_archive(filename,directory):
  if(filename.lower().find(".zip") != -1):
    subprocess.call(["unzip","-d",directory,filename])
  elif(filename.lower().find(".rar") != -1):
    subprocess.call(["unrar","x",filename,directory])
  elif(filename.lower().find(".7z") != -1):
    subprocess.call(["7z","x",filename,"-o"+directory])
  elif(filename.lower().find(".tar.gz") != -1):
    print("Warning: tar.gz extraction is currently not implemented")

