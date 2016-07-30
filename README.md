# 389ds-python-scripts
389 directory server scripts, written in python3. I will update this document as I add more scripts and features. 

##################################################### olc-to-389.py #############################################################

- General Purpose: parses openldap schema files, and reformats them into 389-ds schema files. takes filename as an argument
- Features (with completion dates)
  -  7/27/16: Initial commit. Includes basic input sanitization and "--help" flag
  -  7/29/16: Small bugfix; added -p flag, which allows user to set load priority of the new file
  
- Planned Features
  - A "-r" flag that allows for the parsing of multiple files at once
    the priority, is set to a default value of 98, which is extremely low priority
  - Possibly a "-t" flag that tests to see if the new file is valid, and opens the log file if it is not. Maybe. 

#################################################################################################################################
