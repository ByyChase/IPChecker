import re, os, csv
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

        try:

            #create connection with the database 
            db = sqlite3.connect(db_file)
            logging.info("Database successfully loaded")

        except Exception as e:

            logging.exception("Unable to connect to database, attempting to create database")
            pass
    
    else:

        try:

            #Creates the database files
            db = sqlite3.connect(db_file)
            #Calls the create_db method to create the database tables 
            create_DB(db.cursor())

        except Exception as e:

            logging.exception("Unable to create database, closing program")
            print("Critial error creating database, see logs for more information.\n\nExiting Program")
            exit()

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
                        Date text,
                        Amount real,
                        UnBudgeted real,
                        Description text,
                        IncomeStatement_ID integer PRIMARY KEY,
                        User_ID int,
                        foreign key(User_ID) references User(User_ID)
                        )""")


    except Exception as error:
        print(e)
    
    return





cont = True
Program_Folder_Path = str(os.path.expanduser('~/Documents') + '/PythonIPChecker')
IP_Address_List = []
IP_Address_Found = 0
regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''

IP_Address_Temp = '0'



#Functions
def main(IP_Address_Temp):

    IP_Address_Found = 0
    CSV_Header_Names = ['IP Address', 'Owner', 'Date of Registration', 'IP Range Owned', 'Times Found in Emails', 'Blocked']

    if cont:
        IP_Address = str(input('Please input an IP address: '))

        if IP_Address.lower == 'exit':
            exit()

        if check(IP_Address):
            pass

        else:
            False

    
    print('\n')

    if IP_Address_Temp == IP_Address:
        Check_Same_IP = input("This is the same address you put in right before this. Did you mean to do that? \n\nInput (Yes/No): ")
        while Check_Same_IP.lower() != 'yes' and Check_Same_IP.lower() != 'no':
            Check_Same_IP = input("\n\tPlease only input Yes or no: ")

        if Check_Same_IP.lower() == 'yes':
            print("\n")

        else:
            print("\nWe will restart the script then")
            main(IP_Address_Temp)

    IP_Address_Temp = IP_Address



    for x in IP_Address_List:
        if x[0] == IP_Address:
            x[4] = int(x[4]) + 1

            if x[4] == 1:

                print('\n\nThe CSV file has been updated with this found IP address.')
                Block = input("Are you going to block this IP address? \n\nInput (Yes/No): ")

                while Block != 'yes' and Block != 'YES' and Block != 'Yes' and Block != 'no' and Block != 'NO' and Block != 'No':
                    Block = input("\n\tPlease only input Yes or no: ")

                if Block == 'Yes' or Block == 'yes' or Block == 'YES':
                    x[5] == '1'
                IP_Address_Found = 1

                IP_Address_Temp = IP_Address

            else:
                print('\nThis address has been found ' + str(x[4]) + ' times already')
                Block = input("Are you going to block this IP address? \n\nInput (Yes/No): ")

                while Block != 'yes' and Block != 'YES' and Block != 'Yes' and Block != 'no' and Block != 'NO' and Block != 'No':
                    Block = input("\n\tPlease only input Yes or no: ")

                if Block == 'Yes' or Block == 'yes' or Block == 'YES':
                    x[5] == '1'
                IP_Address_Found = 1

                IP_Address_Temp = IP_Address


    if IP_Address_Found == 0:
        IP_data = ipwhois.IPWhois(IP_Address).lookup_rdap()
        IPList = [IP_data.get('query'), IP_data.get('asn_description'), IP_data.get('asn_date'), IP_data.get('asn_cidr'), '1', '0']
        IP_Address_List.append(IPList)
        print("\nThe IP Address has been added to the CSV file")


    """
    What is in the CSV
    0 IP Address
    1 ASN Description 
    2 ASN Date
    3 ASN IP Range
    4 Times Found 
    5 Blocked

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


main()









