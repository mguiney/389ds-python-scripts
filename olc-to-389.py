#!/usr/bin/python3

###################################################################
#  olc to 389 schema formatting script, implemented in python 3   #
#  written by Megan Guiney                                        #
#  includes help flag, more features to come                      #
###################################################################
import sys
import os
import re
import argparse
import glob
from ldap3 import * 
from shutil import copy

def test_schema(newfile):
  destpath = glob.glob('/etc/dirsrv/slapd-*/schema/')
  errpath = glob.glob('/var/log/dirsrv/slapd-*/errors')
  destpath = destpath[0]
  copy(newfile, destpath)
  s = Server('test389.cat.pdx.edu', get_info=ALL)
  c = Connection(s, user='cn=admin,dc=cat,dc=pdx,dc=edu',password='53JU/\N!')
  if c.bind(): 
    print("Schema successfully added and tested.")   
  else: 
    print("Schema conversion unsuccessful. outputting error logs to screen: ")
    with open(errpath, 'r') as dumplogs: 
      print dumplogs.read()
      dumplogs.close()
    os.chdir(destpath)
    os.remove(newfile)
  

def parse_args():
  parser = argparse.ArgumentParser(description = 'Automatically translates OpenLdap schema files to 389-ds format.')
  parser.add_argument('filename', metavar='F', type=str, nargs='+', help='Name of file to be converted.')
  parser.add_argument('-p', '--priority', dest='priority', action='store', default='98', type=int, help='Specifiy the priority level of the new 389 schema file')
  parser.add_argument('-t', '-test', dest ='test', action='store', default='no', help='Check if the addition of the new schema breaks anything.')
  args = parser.parse_args()
  filename = str(args.filename[0])
  priority = str(args.priority)
  test = str(args.test)
  return filename, priority, test
    

def translate(entries, newfile):
  #gonna give it a static dn, since all schema files have the same dn in 389
  outfile = open( newfile , 'a')
  outfile.write("dn: cn=schema")
  outfile.close()
  #now let's pass through and fix every line, then append them to our new file
  for x in entries:
    x = reformat(x)
    x = str(x)
    outfile = open( newfile , 'a')
    outfile.write(x); outfile.write('\n')
    outfile.close()


def reformat(x):
  #first removing curly bracketed numerical prefixes
  x = re.sub('{.*?}', '', x)
  #eliminate odd spacings
  x = re.sub(' +', ' ', x)
  # remove last remnants of olc format and replace them with empty comments
  # (389 schemas don't like whitespace outside of parens)
  if 'SchemaConfig' in x: 
    return ' ' 
  elif '#' in x:
    delim = '#'
    return x.split(delim, 1)[0]
  elif x == ' +':
    return '#'
  else: 
    return (x) 

def makefile(filename, priority):
  filename = filename[3:]
  newfile = priority + filename
  file = open( newfile, "w")
  file.close()
  return newfile 

def main():
  filename, priority, test = parse_args()
  ldif_chk = ".ldif"
  if ldif_chk in filename: 
    newfile = makefile(filename, priority)
    fileinput = open (filename)
    #going to elim the newlines because the are, for the moment, irrelevant
    with open(filename) as fileinput:
      lines = fileinput.read().replace('\n', ' ')
    #now i'm going to split this mess by the olc delim, and send it to be parsed, modded, and transferred 
    entries = re.split('olc', lines)
    translate(entries, newfile)
    fileinput.close()
    #now (maybe) add it in with the 0ther 389 schema and test
    if test == 'yes': 
      test_schema(newfile)
  else:
    print("ERROR: This is not an ldif file")


main()
