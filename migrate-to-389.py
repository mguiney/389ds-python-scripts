#!/usr/bin/python3

from ldap3 import *
import os
from subprocess import * 

def populate_tree(newfile, new_serv, usrname, pswd):
  #first we define and bind to our new server
  global newconn
  s = Server(new_serv, get_info=ALL)
  c = Connection(s, user = usrname, password = pswd)
  if not c.bind():
    print('error in bind', c.result)
  result = Popen(["ldapadd", "-h", new_serv, "-D", usrname, "-w", pswd, "-f", newfile], stdout=PIPE)
  print result
  

def get_creds(): 
  new_serv = str(raw_input("Enter the fully qualified hostname of the server you are migrating to: "))
  usrname = str(raw_input("Enter the fully qualified dn of the admin user you will be using to build your tree: "))
  pswd = str(raw_input("Enter the password of the admin user you entered above:"))
  return new_serv, usrname, pswd

def ldif_cleanup(filename):
  newfile = filename[1:] 
  nfo = open(newfile, "a")
  with open(filename) as oldfile:  
    for line in oldfile: 
      if '#' in line: 
        line = "\n"
      elif 'version:' in line: 
        line = "\n" 
      nfo.write(line)
  nfo.close()
  return newfile

def branchscrape(x, filename):
  i = 0
  fo = open( filename, "a")
  c.search(search_base = x,
           search_filter = '(!(aci=*))',
           search_scope = SUBTREE,
           attributes = [ALL_ATTRIBUTES])
  while i < len(c.entries):
    fo.write(str(c.entries[i].entry_to_ldif()))
    i = i + 1
  newfile = ldif_cleanup(filename)
  os.remove(filename)
  return newfile

def get_filename(x):
  x = x[3:]
  x = x.split(',',1)[0]
  filename = "_" + x.lower() + ".ldif"
  return filename

def get_branches():
  branches = []
  c.search(search_base = 'dc=cat,dc=pdx,dc=edu',
           search_filter = '(!(cn=*))',
           search_scope = LEVEL,
           attributes = 'dn')
  for branch in c.response:
    branches.append(str(branch['dn']))
  return branches

def bind():
  global c
  s = Server('test389.cat.pdx.edu', get_info=ALL)
  c = Connection(s, user='cn=admin,dc=cat,dc=pdx,dc=edu', password='SECRET_PASSWORD')
  if not c.bind():
    print('error in bind', c.result)

def main():
  bind()
  branches = get_branches()
  new_serv, usrname, pswd = get_creds()
  for x in branches:
    filename = get_filename(x)
    newfile = branchscrape(x, filename)
    populate_tree(newfile, new_serv, usrname, pswd)


main()
