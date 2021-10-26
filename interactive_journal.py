import time,json,datetime

DATAFILE = 'interactive_journal_data.json'

def main():
    #read username data
    data = read_data_file()
    while True:
        #ask for name
        print('Hello. What is your name? ')
        name = input()
        pw = ''
        #ask to make account if they are new
        if name == 'quit':
            quit()
        elif name not in data:
            pw = create_user(name)
            data[name] = {}
            userdata = data[name]
        else:
            print('Glad to see you\'ve returned. Please enter your password: ')
            pw = input()
            userdata = decryption(data[name],pw)
        #loop through asking what they would like to do even if they're new:
        logged_in = True
        while logged_in:
            print('What would you like to do? ')
            help = '(1) Create an entry \n(2) Read an entry \n(3) Delete an entry\n'
            help += '(4) Log out \n(5) Delete account \n(6) Quit'
            print(help)
            inp = input()
            if inp in ['1','c']:
                #make new entry or change one
                create_entry(userdata)
            elif inp == '2' or inp == 'r':
                #read an entry
                read_entry(userdata)
            elif inp in ['3','d']:
                #delete an entry
                delete_entry(userdata)
            elif inp == '4' or inp == 'l':
                #log out
                logged_in = False
            elif inp == '5' or inp == 'd':
                #delete account
                 print("You don't GET to delete your account. Ha. ")
            elif inp == '6' or inp == 'q':
                print('Goodbye...')
                quit_program(userdata,name,pw)
            else:
                print('This option does not exist.')
            print('(Saving changes made so far)')
            save(userdata,name,pw)

"""
ORGANIZATION OF JOURNAL DATA:
{name1:{date1:[{people:,memory:,feeling},{people:,mem:,feel:}]},name2...}
password will not be stored, but eventually, a certain string will
be tested during the decryption to see if it equals the original string
Encryption will skip these characters: "{}:,
"""
def quit_program(userdata:dict, name:str, pw:str):
    save(userdata, name, pw)
    quit()

def save(userdata:dict, name:str, pw:str):
    """
    It is assumed that this data file has already been read before
    and is therefore readable.
    """
    with open(DATAFILE,'r') as file1:
        #get original data
        data = dict(json.load(file1))
    with open(DATAFILE,'w') as file1:
        #add new userdata to it.
        data[name] = encryption(userdata,pw)
        json.dump(data,file1)

# Implement this function at beta run.
def sprint(string:str):
    '''This prints a string slowly, one character at a time.'''
    for i in range(len(string)):
        print(string[i],end='',flush=True)
        time.sleep(.04)
        if(string[i]==','):
            time.sleep(.2)
        if(string[i]=='?' or string[i]=='.'):
            time.sleep(.7)
    time.sleep(1.4)
    print()

def encryption(data,pw):
    data=str(data)
    data2=list([c for c in data])
    pw = list([c for c in pw])
    for c in range(len(data2)):
        data2[c] = ord(data2[c])
        try:
            data2[c] += ord(pw[c%len(pw)])
        except ZeroDivisionError:
            print('A ZeroDivisionError occurred, and data could not be encrypted.')
        data2[c] = chr(data2[c])
    data2 = "".join(data2)
    return data2

def decryption(data,pw):
    try:
        data=str(data)
        data2=list([c for c in data])
        pw = list([c for c in pw])
        for c in range(len(data2)):
            data2[c] = ord(data2[c])
            data2[c] -= ord(pw[c%len(pw)])
            data2[c] = chr(data2[c])
        data2 = "".join(data2)
        #For some odd reason, commas in a value interfere with the json reader
        #so we need double-quotes to fix it, which makes perfect sense.
        data2 = data2.replace("'",'"')
        return json.loads(data2)
    except:
        print('The password entered was incorrect.')
        return data

def create_user(name:str):
    """
    Takes a person's name (first and last or first) and gets and returns 
    their desired password
    """
    #currently only accepts one or two given names
    if name.find(' ') != -1:
        first_name = name[:name.find(' ')]
        #last_name = name[name.find(' ')-1:] #not used
    else:
        first_name = name
    #store password
    print(f'It looks like you are new here. Pleased to meet you, {first_name}.')
    print('Please enter a password. This will be used to keep all your entries to yourself.')
    password = input()
    print('Password accepted. Now, don\'t forget this password, or your entries will be unreadable.')
    return password

def read_entry(data:dict):
    """
    Prints out all the memories stored in a date that is asked for.
    """
    print('What date of entry would you like to access? ')
    date = input()
    date = date_parser(date)
    if date in data:
        for memset in data[date]:
            print('On',date,'you were with',memset['people'],'and this is what happened: ')
            print(str(memset['memory']).capitalize())
            print('It made you feel',str(memset['feeling']).lower() + '.')
        
    else:
        print('No entries exist under this date. ')
        print('Showing entries that do exist: ')
        for date in data:
            print(date)

def create_entry(data:dict):
    """
    This will add a dictionary of 1 key (the date) and 1 value, which will be
    a list of dictionaries, or memories, each with 3 key-value pairs. It will
    return this with the rest of data
    """
    #store date
    print('What is the date of this memory? (put "today" if it\'s today) ')
    date = input()
    date = date_parser(date)
    #loop through memory adding
    memorylist = []
    newmemory = True
    while newmemory:
        # store data to mem_dict as you go
        mem_dict = dict()
        #store who was with you
        print('Who was with you in this memory? ')
        mem_dict['people'] = input()
        #store a memory
        print('And tell me, what happened? ')
        mem_dict['memory'] = input()
        #store how it made you feel
        print('In a word, how did this make you feel? ')
        mem_dict['feeling'] = input()

        memorylist.append(mem_dict)
        print('Thank you for sharing this memory with me. I shall store it for as long as you like. ')
        print('Do you have another memory from this day? (yes or no) ')
        newmemory = (input() == 'yes')
    #add to the current list of memories if an entry for this day already exists:
    if date in data:
        data[date] += memorylist
    else:
        data[date] = memorylist
    return data

def delete_entry(userdata:dict):
    print('What is the date of this memory? (put "today" if it\'s today) ')
    date = input()
    date = date_parser(date)
    print('Would you like to read it before deleting it? (yes or no) ')
    if (input() == 'yes'):
        print(userdata[date])
    print('Are you sure you want to delete this entry? (yes or no) ')
    if (input() == 'yes'):
        del userdata[date]
        print('Entry deleted.')

def date_parser(date):
    """
    Takes most any date format and returns it in 'MM DD YYYY' format
    """
    if len(date) < 3:
        return 'Invalid Date'
    elif date == 'today':
        date = str(datetime.datetime.today().strftime('%m %d %Y')) #10 25 2021
    #convert date string to a list to allow easier changing
    datelist = [c for c in date]
    i = 0
    # Periods and commas are ignored/removed.
    while i != len(datelist):
        if datelist[i] == '.' or datelist[i] == ',':
            del datelist[i]
        else:
            # Spaces, slashes, and dashes are interchangeable.
            if datelist[i] == '/' or datelist[i] == '-':
                datelist[i] = ' '
            i += 1
    date = "".join(datelist)
    # The month will always be shorter than 3 if it is a number
    # October or Oct -> 10
    if date.index(' ') > 2:
        date = date.lower()
        months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        if date[:3] in months:
            date = str(months.index(date[:3]) + 1) + date[date.index(' '):]
        # If they don't give the year, assume it is this year
    if len(date) < 8:
        date += ' ' + datetime.datetime.today().strftime('%Y')
    print('Parsed date:',date)
    return date

def read_data_file():
    """
    return the contents of interactive_journal_data.txt as a dictionary
    """
    datadict = dict()
    with open(DATAFILE,'r') as file1:
        print('Attempting to load file as a JSON...')
        try:
            datadict = json.load(file1)
            print('JSON data loaded succesfully.')
        except:
            print('Data file is empty. Writing an example data file now.')
            datadict['name'] = {'10 25 2021':[{'people':'no one','memory':'nothing','feeling':'blank'}]}
    with open(DATAFILE,'w') as file1:
        json.dump(datadict,file1)
    return datadict

main()