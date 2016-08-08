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
  
  - General Purpose: to migrate the contents of an existing 389 directory to a new ds. prompts user for details of this server
  - Features/Commits (with completion dates)
    -  8/3/16: Initial commit. Still very quirky, doesn't have full functionality
    -  8/5/16: now checks to see if 389-ds is running to a server specified by the user, and rebuilds the tree on that ds if the    service is, in fact, running. 
  
  -  Planned Features: 
    - I want this taking nearly all user input from the command line. This includes: 
      - a "-s" flag that indicates the domain name of the new server
      - a "-u" flag that indicates the dn of the admin user that the script will be ldapadd-ing as 
      - a "-p" flag that passes in the password needed to authenticate as the admin user listed above 
    
  
################################################################################################################################
