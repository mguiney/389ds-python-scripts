# 389ds-python-scripts
389 directory server scripts, written in python3. I will update this document as I add more scripts and features. 

                                                olc-to-389.py 

- General Purpose: parses openldap schema files, and reformats them into 389-ds schema files. takes filename as an argument
- Features/Commits (with completion dates)
  -  7/27/16: Initial commit. Includes basic input sanitization and "--help" flag
  -  7/29/16: Small bugfix; added -p flag, which allows user to set load priority of the new file
  
- Planned Features
  - A "-r" flag that allows for the parsing of multiple files at once
    the priority, is set to a default value of 98, which is extremely low priority
  - Possibly a "-t" flag that tests to see if the new file is valid, and opens the log file if it is not. Maybe. 

#################################################################################################################################
                                                migrate-to-389.py
  
  - General Purpose: to migrate the contents of an existing 389 directory to a new ds. prompts user for details of this server
  - Features/Commits (with completion dates)
    -  8/3/16: Initial commit. Still very quirky, doesn't have full functionality
  
  -  Planned Features 
    - Basically, I want this taking nearly all user input from the command line. This includes: 
      - a "-s" flag that indicates the domain name of the new server
      - a "-u" flag that indicates the dn of the admin user that the script will be ldapadd-ing as 
      - a "-p" flag that passes in the password needed to authenticate as the admin user listed above
    - Will also be adding a "--help" flag that lists the functionality of the above flags, for obvious reasons. 
  
################################################################################################################################
