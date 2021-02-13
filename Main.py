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

    statement = "FROM IPADDRESS SELECT * WHERE IP_ADDRESS = ?"
    ip_address_data = cursor().execute(statement, (ip_address, description, ip_range, date, times_found, blocked)).fetchone()

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


    IP_data = ipwhois.IPWhois(IP_Address).lookup_rdap()
    IPList = [IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_date'), IP_data.get('asn_cidr'), '1', '0']

    if fetch(IP_data.get('query')):
        print("This address has already been added to the database")

    else:
        commit_ip_address(IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_cidr'), IP_data.get('asn_date'), '1', '0')
        print("\n\n------------------------------------------\n|The following entry has been added to the database|\n------------------------------------------: ")
        print("IP Address: " + IPList[0] + + "\nIP Range: " + IPList[3] + "\nDescription: " + IPList[1] + "\nDate: " + IPList[2]) 
        print("\n\nThe IP Address has been added t o the database")


    

    


 
    Repeat = input("Would you like to add another IP Address? \n\nInput (Yes/No):")
    while Repeat != 'yes' and Repeat != 'YES' and Repeat != 'Yes' and Repeat != 'no' and Repeat != 'NO' and Repeat != 'No':
        Repeat = input("\n\tPlease only input Yes or no: ")

    if Repeat == "no" or Repeat == "NO" or Repeat == "No":
        exit()

    else:
        main()


print(" __   ______        ______  __    __   _______   ______  __  ___  _______  ______")      
print("|  | |   _  \      /      ||  |  |  | |   ____| /      ||  |/  / |   ____||   _  \ ")    
print("|  | |  |_)  |    |  ,----'|  |__|  | |  |__   |  ,----'|  '  /  |  |__   |  |_)  | ")   
print("|  | |   ___/     |  |     |   __   | |   __|  |  |     |    <   |   __|  |      / ")    
print("|  | |  |         |  `----.|  |  |  | |  |____ |  `----.|  .  \  |  |____ |  |\  \----. ")
print("|__| |__|          \ _____||__|  |__| |_______| \______||__|\__\ |_______|| _| `._____| ")
print("Please type 'Exit' at anytime to quit the program\n")

try:
    load_DB(os.getcwd() + '/ip_checker.db')

except Exception as e:
    print("\n\nCould not load Database")
    print("\n\n" + str(e))


main()









