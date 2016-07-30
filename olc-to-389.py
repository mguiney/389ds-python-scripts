#!/usr/bin/python3

###################################################################
#  olc to 389 schema formatting script, implemented in python 3   #
#  written by Megan Guiney (Valkyrie, to any Katzen seeing this)  #
#  includes help flag, more features to come                      #
###################################################################

import re
import sys

def help():
    print("This script parses olc-format LDIFs and converts them to 389 format")
    print("It takes one argument, and that is the olc-formatted LDIF you wish to use")
    print("--help:  help flag; spits out command description and flags.")
    print("-p:      load flag; sets schema loading priority for the new file.")
    

def translate(entries, newfile):
    #gonna give it a static dn, since all schema files have the same dn in 389
    outfile = open( newfile , 'a')
    outfile.write("dn: cn=schema"); outfile.write('\n')
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
      return '#' 
    elif '#' in x:
      delim = '#'
      return x.split(delim, 1)[0]
    else: 
      return (x) 

def makefile(filename):
    filename = filename[3:]
    newfile = priority + filename
    file = open( newfile, "w")
    file.close()
    return newfile 

def main():
  #if the user enters a helpflag, kick them into an explanation 
  if len(sys.argv) < 2:  
    print ("No input. Exiting script. ")
    sys.exit()  
  elif str(sys.argv[1]) == "--help":
    help()
  else:
    if str(sys.argv[2]) == "-p" :
      priority = str(sys.argv[3])
    else:
      priority = 98
    filename = sys.argv[1]
    ldif_chk = ".ldif"
    if ldif_chk in filename: 
      #make file using the filename
      newfile = makefile(filename)
      #next create file object 
      fileinput = open (filename)
      #start separating entries from the olc ldif to be parsed
      #first i'm going to elim the newlines because the are, for the moment, irrelevant
      with open(filename) as fileinput:
        lines = fileinput.read().replace('\n', ' ')
      #now i'm going to split this mess by the olc delim, and send it to be parsed, modded, and transferred 
      entries = re.split('olc', lines)
      translate(entries, newfile)
      fileinput.close()
    else:
      print("ERROR: This is not an ldif file")


main()
