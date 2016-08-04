#!/usr/bin/python3

from ldap3 import *
import os
import scp

def migrate(files): 
  # get user input
  hostname = input("Enter the hostname you are migrating your directory tree to:  ")
  username = input("Enter the dn of the admin user of your new ds: ") 
  targetdir = input("Enter the path of the directory in which you would like to place the files:  ")
  # prep the target server for migration
  configure()
  # scp over the files 
  client = scp.Client(host= hostname, user= username)
  client.use_system_keys()
  for x in files
    client.transfer( x , targetdir )


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
  c = Connection(s, user='cn=admin,dc=cat,dc=pdx,dc=edu', password='53JU/\N!')
  if not c.bind():
    print('error in bind', c.result)

def main():
  files = []
  bind()
  branches = get_branches()
  for x in branches:
    filename = get_filename(x)
    newfile =  branchscrape(x, filename)
    files.append(newfile)
  migrate(files) 

main()
