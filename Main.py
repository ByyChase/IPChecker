import re, os 
  
# Make a regular expression
# for validating an Ip-address
regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
cont = True
Program_Folder_Path = str(os.path.expanduser('~/Documents') + '/PythonIPChecker')
print(Program_Folder_Path)

# Define a function for
# validate an Ip addess
def check(IP_Address):

    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, IP_Address)):
        return True

    else:
        return False

if cont:
    IP_Address = str(raw_input('Please input an IP address: '))

    if check(IP_Address):
        pass

    else:
        False

if not os.path.exists(Program_Folder_Path):
    os.makedirs(Program_Folder_Path)






