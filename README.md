# 389ds-python-scripts
389 directory server scripts, written in python3. I will update this document as I add more scripts and features. 

                                                olc-to-389.py 

  - General Purpose: parses openldap schema files, and reformats them into 389-ds schema files. takes filename as an argument

  - Features/Commits (with completion dates)
    -  7/27/16: Initial commit. Includes basic input sanitization and "--help" flag
    -  7/29/16: Small bugfix; added -p flag, which allows user to set load priority of the new file
    -  8/4/16:  Another small bugfix; switched from manual flag parsing to using argparse
    -  8/7/16:  Added a -t flag that allows you to test if the schema breaks the server, and removes it if it does
  
  - Planned Features
    - A "-r" flag that allows for the parsing of multiple files at once


#################################################################################################################################
                                                migrate-to-389.py
  
  - General Purpose: to migrate the contents of an existing directory to a new ds. prompts user for details of this server
  
  - Features/Commits (with completion dates)
    -  8/3/16: Initial commit. Still very quirky, doesn't have full functionality
    -  8/5/16: now checks to see if 389-ds is running to a server specified by the user, and rebuilds the tree on that ds if the    service is, in fact, running.
    -  8/9/16: all destination server info is taken as command line arguments 
    -  1/5/17: no longer uses the library that truncates lines. back in a working state. 
  
  -  Planned Features: 
    - Add user I/O option flag that prompts the user for server/administrator details rather than taking them as a command line option.  
    - integrating the schema conversion script above so that: 
        - you can be sure your schemas have been reformatted , transferred, and tested properly
        - the process becomes less complicated as a whole for the user
	- this will be implemented as a flag, so that it is not mandatory
  
  -  Usage notes:
    - This script is meant to be run on the server you are migrating the directory tree from, not the one you are migrating it to. 
    - The ds you are migrating it to must have a pubkey from the source server, and you should start an ssh agent ahead of time.  
    - If you have custom schema, please add them previous to running this script.
    - for more information on flags, use the -h or --help option while running the script
   
################################################################################################################################
