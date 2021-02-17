import re, os, csv, sqlite3
import ipwhois


#Validate IP Address
def check(IP_Address):

    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, IP_Address)):
        return True

    else:
        return False

db = None


def load_DB(db_file):
    """
    This function is used to load the database at program start.
    ...
    Parameters
    ----------
    db_file : string
        The location that the database file should be. It should be located in the root directory of the program
    ...
    Returns
    -------
    db.cursor() : function
        This calls the cursor function that returns the cursor for the database
    """

    global db
    
    #Checks to see if the database file exists. If it does not the database will be created 
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

    try:
        c.execute("""CREATE TABLE IPADDRESS (
                        IP_ADDRESS text PRIMARY KEY,
                        DESCRIPTION text,
                        IP_RANGE test,
                        DATE text,
                        TIMES_FOUND text,
                        BLOCKED text
                        )""")


    except Exception as error:
        print(e)
    
    return

def commit_ip_address(ip_address, description, ip_range, date, times_found, blocked):

    statement = "INSERT INTO IPADDRESS (IP_ADDRESS, DESCRIPTION, IP_RANGE, DATE, TIMES_FOUND, BLOCKED) VALUES (?, ?, ?, ?, ?, ?)"
    cursor().execute(statement, (ip_address, description, ip_range, date, times_found, blocked))
    commit()


def fetch(ip_address):

    statement = "SELECT * FROM IPADDRESS WHERE IP_ADDRESS = ?"
    ip_address_data = cursor().execute(statement, (ip_address,)).fetchone()

    if ip_address_data: 
        return ip_address_data
    
    else:
        return "0"


def update(number, which_number):

    if which_number == "1":
        pass

    elif which_number == "2":
        pass


regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''


#Functions
def main():


   
    IP_Address = str(input('Please input an IP address: '))

    if IP_Address.lower == 'exit':
        exit()

    if check(IP_Address):
        pass

    else:
        False

    
    print('\n')

    try:
        IP_data = ipwhois.IPWhois(IP_Address).lookup_rdap()

    except:
        print("\n\n\t\tLooks like there was an error with the address you entered, lets re run it\n\n")
        main()

    IPList = [IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_date'), IP_data.get('asn_cidr'), '1', '0']

    data = fetch(IP_data.get('query'))

    print(data)


    if data != "0":

        print("This address has already been added to the database")
        print("\n\nHere is the info on the info from the IP Address")
        print("\nIP Address: " + data[0] + "\nIP Range: " + data[2] + "\nDescription: " + data[1] + "\nDate: " + data[3] + "\nTimes Found: " + str(int(data[4]) + 1) + "\nBlocked: " + isBlocked(data[5]))
        blocked = input("\nAre you going to block this IP address? \n\nInput (Yes or No): ")
       


    else:

        commit_ip_address(IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_cidr'), IP_data.get('asn_date'), '1', '0')
        print("\n\n------------------------------------------\n|The following entry has been added to the database|\n------------------------------------------: ")
        print("IP Address: " + IPList[0] + "\nIP Range: " + IPList[3] + "\nDescription: " + IPList[1] + "\nDate: " + IPList[2]) 
        print("\n\nThe IP Address has been added t o the database")


    

    


 
    Repeat = input("Would you like to add another IP Address? \n\nInput (Yes/No):")
    while Repeat != 'yes' and Repeat != 'YES' and Repeat != 'Yes' and Repeat != 'no' and Repeat != 'NO' and Repeat != 'No':
        Repeat = input("\n\tPlease only input Yes or no: ")

    if Repeat.lower() == "no":
        exit()

    else:
        print("\n\n")
        main()


print(" __   ______        ______  __    __   _______   ______  __  ___  _______  ______")      
print("|  | |   _  \      /      ||  |  |  | |   ____| /      ||  |/  / |   ____||   _  \ ")    
print("|  | |  |_)  |    |  ,----'|  |__|  | |  |__   |  ,----'|  '  /  |  |__   |  |_)  | ")   
print("|  | |   ___/     |  |     |   __   | |   __|  |  |     |    <   |   __|  |      / ")    
print("|  | |  |         |  `----.|  |  |  | |  |____ |  `----.|  .  \  |  |____ |  |\  \----. ")
print("|__| |__|          \ _____||__|  |__| |_______| \______||__|\__\ |_______|| _| `._____| ")
print("\nPlease type 'Exit' at anytime to quit the program\n")

try:
    load_DB(os.getcwd() + '/ip_checker.db')

except Exception as e:
    print("\n\nCould not load Database")
    print("\n\n" + str(e))


main()









