import re, os, csv, sqlite3
import ipwhois
from tkinter import filedialog

#Define Global Variables 
regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
db = None



#--------------------------- Functions -----------------------------------------

def check(IP_Address):
    """
    This method is used to check if an IP address is formated correctly. It uses
    Regex which I do not understand at all and got off of Stack Overflow. It 
    seems to work so I just don't really touch this method at all.

    Parameters:
    -----------
    IP_Address: String 
        This string holds an IP address that is entered by the user

    Returns:
    --------
    Boolean: 
        If the IP Address the user entered is formated correctly then True is
        returned. If it is not correctly formated then False is returned 

    """

    if(re.search(regex, IP_Address)):
        return True

    else:
        return False

def load_DB(db_file):
    """
    This function is used to load the database at program start.
    ...
    Parameters
    ----------
    db_file : string
        The location that the database file should be. It should be located in 
        the root directory of the program
    ...
    Returns
    -------
    db.cursor() : function
        This calls the cursor function that returns the cursor for the database
    """

    global db
    
    #Checks to see if the database file exists. If it does not the database 
    # will be created 
    if os.path.isfile('ip_checker.db'):

       

        #create connection with the database 
        db = sqlite3.connect(db_file)
    
    else:

        #Creates the database files
        db = sqlite3.connect(db_file)
        #Calls the create_db method to create the database tables 
        create_DB(db.cursor())


    return db.cursor()

def isBlocked(Blocked): 
    """
    This method is used to check to see if an IP Address is blocked or not. This
    is a very simple method used to save code. 

    Parameters:
    -----------
    Blocked: integer
        This integer holds 0 or 1. 0 for False and 1 for True

    Returns:
    --------
    Boolean:
        If the integer provided is 0, False is returned. If the integer is 1,
        True is returned 
    """

    if Blocked == "0":
        return "False"

    else:
        return "True"

def cursor():
    """
    This function is used to retreive the database cursor
    ...
    Returns
    -------
    db.cursor() : function
        This calls the cursor function that returns the cursor for the database
    """

    if not db:
        LoadDB()

    else:
        return db.cursor()

def commit():
    """
    This method is used to commit the database
    """

    db.commit()

def close():
    """
    This method is used to close the database connection
    """

    db.close()

def create_DB(c):
    """
    This Method is used to create the database. If the database already exists 
    this method will not run 

    Parameters:
    -----------
    c: cursor object 
        This is the cursor object created for the database. 
    """

    try:
        c.execute("""CREATE TABLE IPADDRESS (
                        IP_ADDRESS text PRIMARY KEY,
                        DESCRIPTION text,
                        IP_RANGE test,
                        DATE text,
                        TIMES_FOUND int,
                        BLOCKED text
                        )""")


    except Exception as error:
        print(e)
    
    return

def commit_ip_address(ip_address, description, ip_range, date, times_found, blocked):
    """
    This method is used to add a new IP address to the database.

    Parameters:
    -----------
    ip_address : String
        This is a validated string holding an IP address entered by the user

    description : String
        Description of the IP address from WHO IS search

    ip_range : String
        The IP range that the IP belongs to 

    date : String
        Date of initial ownership

    times_found : integer
        the number of times that the IP address has been run through the program

    """
    #SQL statement
    statement = "INSERT INTO IPADDRESS (IP_ADDRESS, DESCRIPTION, IP_RANGE, DATE, TIMES_FOUND, BLOCKED) VALUES (?, ?, ?, ?, ?, ?)"
    #Execute the SQL statement
    cursor().execute(statement, (ip_address, description, ip_range, date, 
    times_found, blocked))
    commit()

def fetch(ip_address):
    """

    This method is used for retreiving the IP address from the datbase. 

    Parameters:
    -----------
    ip_address : String
        This is a validated IP address entered in by the user. It is the primary
        key in the database. It will be used to fetch all of the data associated
        with the IP address
    """

    #SQL statement
    statement = "SELECT * FROM IPADDRESS WHERE IP_ADDRESS = ?"
    #Execture the SQL statement
    ip_address_data = cursor().execute(statement, (ip_address,)).fetchone()

    #If the IP address is in the database it will return the data associated
    if ip_address_data: 
        return ip_address_data
    
    #If nothing is returned, 0 is returned
    else:
        return "0"

def update(ip_address, description, ip_range, date, times_found, blocked):
    """
    This method is used to update the IP Address listing in the database. This 
    really is only used to update if it is blocked or how many times the IP 
    address has been found

    Parameters:
    -----------
    ip_address : String
        This is a validated string holding an IP address entered by the user

    description : String
        Description of the IP address from WHO IS search

    ip_range : String
        The IP range that the IP belongs to 

    date : String
        Date of initial ownership

    times_found : integer
        the number of times that the IP address has been run through the program
    """

    #SQL statement
    statement = "UPDATE IPADDRESS SET DESCRIPTION = ?, IP_RANGE = ?, DATE = ?, TIMES_FOUND = ?, BLOCKED = ? WHERE  IP_ADDRESS = ?"
    #Execute the SQL statement
    cursor().execute(statement, (description, ip_range, date, times_found, blocked, ip_address))
    commit()

#----------------------------- Main Code ---------------------------------------

def main():

    IP_Address = str(input('Please input an IP address: '))

    if IP_Address.lower() == 'exit':
        exit()

    elif IP_Address.lower() == 'export':
        print("\n\nexport")
        main()

    if check(IP_Address):
        pass

    else:
        print("\n\n\t\tLooks like there was an error with the address you entered, lets re run it\n\n")
        main()

    
    print('\n')

    try:

        IP_data = ipwhois.IPWhois(IP_Address).lookup_rdap()

    except:

        print("\n\n------------ ERROR ------------\nThere was a problem reaching out to the API\n\Restarting Scriptn\n")
        main()

    IPList = [IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_date'), IP_data.get('asn_cidr'), '1', '0']

    data = fetch(IP_data.get('query'))

    print(data)


    if data != "0":

        print("This address has already been added to the database")
        print("\n\nHere is the info on the info from the IP Address")
        TimesFound = data[4] + 1

        if isBlocked(data[5]) == "True":

            print("\n-------- THIS ADDRESS HAS BEEN BLOCKED --------")

        print("\nIP Address: " + data[0] + "\nIP Range: " + data[2] + "\nDescription: " + data[1] + "\nDate: " + data[3] + "\nTimes Found: " + str(TimesFound) + "\nBlocked: " + isBlocked(data[5]))

        if isBlocked(data[5]) == 'False':

            blocked = input("\nAre you going to block this IP address? \n\nInput (Yes or No): ")

            while blocked.lower() != 'yes' and blocked.lower() != 'no' and blocked.lower() != 'exit' and blocked.lower() != 'export':

                blocked = input("\nPlease only input an accepted input! \n\nInput (Yes or No): ")


            if blocked.lower() == 'yes':

                update(data[0], data[1], data[2], data[3], TimesFound, '1')
                print('\n\n--------- THE ADDRESS HAS BEEN BLOCKED --------')

            elif blocked.lower() == 'exit':

                exit()

            elif blocked.lower() == 'export':

                print("\n\n export")
                main()
            

            else:

                print('updating database' + '\n' + str(TimesFound))
                update(data[0], data[1], data[2], data[3], TimesFound, '0')
  
    else:

        print("\n ------------------------------------\n| Here is the IP Address Information |\n ------------------------------------\n")
        print("IP Address:  " + IPList[0] + "\nIP Range:    " + IPList[3] + "\nDescription: " + IPList[1] + "\nDate:        " + IPList[2]) 

        blocked = input("\nAre you going to block this IP address? \n\nInput (Yes or No): ")

        while blocked.lower() != 'yes' and blocked.lower() != 'no' and blocked.lower() != 'exit' and blocked.lower() != 'export':

                blocked = input("\nPlease only input an accepted input! \n\nInput (Yes or No): ")

        if blocked.lower() == 'yes':

            commit_ip_address(IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_cidr'), IP_data.get('asn_date'), 1, '1')
            print('\n\n--------- THE ADDRESS HAS BEEN BLOCKED --------')

        elif blocked.lower() == 'exit':

                exit()

        elif blocked.lower() == 'export':

                print("\n\n export")
                main()      

        else:

            commit_ip_address(IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_cidr'), IP_data.get('asn_date'), 1, '0')

    print("\n\n ---------------------------------------------\n|The IP Address has been added to the database|\n ---------------------------------------------\n")
 
    Repeat = input("\n\nWould you like to add another IP Address? \n\nInput (Yes/No):")

    while Repeat != 'yes' and Repeat != 'YES' and Repeat != 'Yes' and Repeat != 'no' and Repeat != 'NO' and Repeat != 'No' and Repeat.lower() != 'exit' and Repeat.lower() != 'export':
        
        Repeat = input("\n\tPlease only input Yes or no: ")

    if Repeat.lower() == "no":

        exit()

    elif Repeat.lower() == "exit":

        exit()
        main()

    elif Repeat.lower() == "export":

        print("\n\nexport")

    else:

        print("\n\n")
        main()


print(" __   ______        ______  __    __   _______   ______  __  ___  _______  ______")      
print("|  | |   _  \      /      ||  |  |  | |   ____| /      ||  |/  / |   ____||   _  \ ")    
print("|  | |  |_)  |    |  ,----'|  |__|  | |  |__   |  ,----'|  '  /  |  |__   |  |_)  | ")   
print("|  | |   ___/     |  |     |   __   | |   __|  |  |     |    <   |   __|  |      / ")    
print("|  | |  |         |  `----.|  |  |  | |  |____ |  `----.|  .  \  |  |____ |  |\  \----. ")
print("|__| |__|          \ _____||__|  |__| |_______| \______||__|\__\ |_______|| _| `._____| ")
print("\n\n\n----------------------------- PROGRAM SUB-OPTIONS -----------------------------\n")
print("Type 'Export' at any time to see all IP Addresses in the database")
print("Type 'Exit' at any time to quit the program\n\n")

try:
    load_DB(os.getcwd() + '/ip_checker.db')

except Exception as e:
    print("\n\nCould not load Database")
    print("\n\n" + str(e))


main()









