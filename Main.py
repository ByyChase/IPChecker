import re, os, csv
import ipwhois

cont = True
Program_Folder_Path = str(os.path.expanduser('~/Documents') + '/PythonIPChecker')
IP_Address_List = []
fieldnames = ['IP Address', ]
IP_Address_Found = 0
CSV_Header_Names = ['IP Address', 'Owner', 'Date of Registration', 'IP Range Owned', 'Times Found in Emails', 'Blocked']
#Functions
def main():

    IP_Address_Found = 0
    CSV_Header_Names = ['IP Address', 'Owner', 'Date of Registration', 'IP Range Owned', 'Times Found in Emails', 'Blocked']

    #Validate IP Address
    def check(IP_Address):

        # pass the regular expression
        # and the string in search() method
        if(re.search(regex, IP_Address)):
            return True

        else:
            return False


    if cont:
        IP_Address = str(input('Please input an IP address: '))

        if check(IP_Address):
            pass

        else:
            False


    if not os.path.exists(Program_Folder_Path):
        os.makedirs(Program_Folder_Path)

    #Opening file to ensure it is created
    IP_Address_File = open(Program_Folder_Path + "/IPFile.csv", "w+")
    #Closing it so I can open it in the correct mode
    IP_Address_File.close() 
    #opening it in the correct mode and taking the data into a list
    with open(Program_Folder_Path + "/IPFile.csv", "r") as IP_Address_File:
        csv_reader = csv.reader(IP_Address_File) 
        for line in csv_reader:
            IP_Address_List.append(line)

        IP_Address_File.close()


    for x in IP_Address_List:
        if x[0] == IP_Address:
            x[4] = int(x[4]) + 1

            print('\n\nThe CSV file has been updated with this found IP address.')
            Block = input("Are you going to block this IP address? \n\nInput (Yes/No): ")

            while Block != 'yes' and Block != 'YES' and Block != 'Yes' and Block != 'no' and Block != 'NO' and Block != 'No':
                Block = input("\n\tPlease only input Yes or no: ")

            if Block == 'Yes' or Block == 'yes' or Block == 'YES':
                x[5] == '1'
            IP_Address_Found = 1

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

    """


    with open(Program_Folder_Path + "/IPFile.csv", "w") as IP_Address_File:
        csv_writer = csv.DictWriter(IP_Address_File, fieldnames = CSV_Header_Names)
        csv_writer.writeheader()

        CSV_Header_Names = ['IP Address', 'Owner', 'Date of Registration', 'IP Range Owned', 'Times Found in Emails', 'Blocked']

        for x in IP_Address_List:
            csv_writer.writerow({'IP Address' : x[0], 'Owner' : x[1], 'Date of Registration' : x[2], 'IP Range Owned' : x[3], 'Times Found in Emails' : x[4], 'Blocked' : x[5]})
            
        IP_Address_File.close()



    Repeat = input("Would you like to add another IP Address? \n\nInput (Yes/No):")
    while Repeat != 'yes' and Repeat != 'YES' and Repeat != 'Yes' and Repeat != 'no' and Repeat != 'NO' and Repeat != 'No':
        Repeat = input("\n\tPlease only input Yes or no: ")

    if Repeat == "no" or Repeat == "NO" or Repeat == "No":
        exit()

    else:
        main()


#Global Variables
regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''



main()









