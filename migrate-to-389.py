#!/usr/bin/python3

from ldap3 import *
import os
import sys
import subprocess
import argparse

def populate_tree(newfile, new_serv, usrname, pswd):
  #first we define and bind to our new server
  global newconn
  s = Server(new_serv, get_info=ALL)
  c = Connection(s, user = usrname, password = pswd)
  if not c.bind():
    print('error in bind', c.result)
  result = subprocess.Popen(["ldapadd", "-h", new_serv, "-D", usrname, "-w", pswd, "-f", newfile], stdout=subprocess.PIPE)
  print result

def test_ldap(new_serv):
  command = "systemctl status target.dirsrv"
  ssh = subprocess.Popen(["ssh", new_serv, command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  result = ssh.stdout.readlines()
  if result == []: 
    error = ssh.stderr.readlines()
    print ("ERROR: " + error)
    return 0 
  else: 
    if "inactive" in result: 
      print("directory server not active. Please restart and try again. ") 
      sys.exit()
    elif "service not found" in result: 
      print("389-ds not installed. Please install and try again. ") 
      sys.exit()
    else: 
      return 1

def parse_args():
  parse = argparse.ArgumentParser(description = 'Migration script for 389-ds replication')
  parse.add_argument('-s', '-new-server', dest='new_serv', action='store', type=str, help='Specifies the hostname you are migrating your tree to. Required.')
  parse.add_argument('-u','-username', dest='usrname', action='store', type=str, help='Specifiesthe fully qualified dn of the admin user you will be repopulating the tree as. ')
  parse.add_argument('-p', '-password', dest='pswd', action='store', type=str, help='Specifies the password of the admin user specified by the "-u" flag')
  args = parse.parse_args()
  new_serv = str(args.new_serv)
  usrname = str(args.usrname)
  pswd = str(args.pswd)
  return new_serv, usrname, pswd

#uncomment for user I/O mode
#will add a flag for this later     
#def get_creds(): 
#  new_serv = str(raw_input("Enter the fully qualified hostname of the server you are migrating to: "))
#  usrname = str(raw_input("Enter the fully qualified dn of the admin user you will be using to build your tree: "))
#  pswd = str(raw_input("Enter the password of the admin user you entered above:"))
#  return new_serv, usrname, pswd

def ldif_cleanup(filename):
  newfile = filename[1:] 
  nfo = open(newfile, "a")
  with open(filename) as oldfile:  
    for line in oldfile: 
      if '#' in line: 
        nfo.write("\n")
      elif 'version:' in line: 
        nfo.write("\n")
      else: 
        nfo.write(line)
  nfo.close()
  return newfile

def branchscrape(x, filename):
  i = 0
  fo = open( filename, "a")
  print "scraping branch with the base: " + x.split('dn:',1)[1] 
  cmd = "ldapsearch -o ldif-wrap=no -xLLL -h haopenldap -D 'uid=you,dc=example,dc=com' -w 'SECRET_PASSWORD' -b " + x.split('dn:',1)[1] + " -s sub"
  search = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
  search = search.split("\n")
  for x in search:
    fo.write(x + "\n")
  fo.close()
  newfile = ldif_cleanup(filename)
  os.remove(filename)
  return newfile

def get_filename(x):
  x = x[7:]
  x = x.split(',',1)[0]
  filename = "_" + x.lower() + ".ldif"
  return filename

def get_branches():
  branches = []
  cmd = "ldapsearch -o ldif-wrap=no -xLLL -h haopenldap -D 'uid=you,dc=example,dc=com' -w 'SECRET_PASSWORD' -b 'dc=example,dc=com' -s one | grep dn"
  search = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
  search = search.split("\n")
  for x in search:
      if 'cn' not in x and x != '': 
        branches.append(x)
  return branches

def bind():
  global c
  s = Server('haopenldap.cat.pdx.edu', get_info=ALL)
  c = Connection(s, user='uid=you,dc=example,dc=com', password='SECRET_PASSWORD')
  if not c.bind():
    print('error in bind')

def main():
  bind()
  branches = get_branches()
  new_serv, usrname, pswd = parse_args()
  for x in branches:
    filename = get_filename(x)
    newfile = branchscrape(x, filename)
    #ldap_chk = test_ldap(new_serv) 
    #if ldap_chk == 1: 
      #populate_tree(newfile, new_serv, usrname, pswd)


main()
