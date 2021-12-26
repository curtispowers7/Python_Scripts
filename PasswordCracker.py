#Author: Curtis Powers
#Intent: Mostly a learning exercise, but also to help with cracking passwords found during pentesting exercises


#Import the libraries needed
import hashlib
import sys
import json
import requests
import argparse

#Define the arguments for the script
parser = argparse.ArgumentParser(description="Lookup Password Hash")
parser.add_argument("--passwordDictionary", type=str)
parser.add_argument("--passwordHash", type=str)
parser.add_argument("--passwordHashArray", nargs="*", type=str)
args = parser.parse_args()


#Create the functions needed throughout the script

#This will create the password dictionary if it doesn't exist on the local file system and it is not passed as an argument
#The file of 10 million top passwords is pulled from github
def createPasswordDictionary ():
    #Create the dictionary list with all the passwords and save it
    print("Downloading password dictionary from: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt")
    url = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt'
    file = requests.get(url).text

    #create an array of passwords from the list
    passwords = list(filter(None,file.split("\n")))

    #create an empty dictionary for the hashes
    dictPasswords = {}

    #the list of supported hashing algorithms
    arrDigests = ['md5', 'sha1', 'sha256', 'sha512']
    
    #loop through the passwords, creating an entry in the dictionary with the hash as the key and the password as the value
    print("Creating password dictionary from password list")
    for password in passwords:
        for digest in arrDigests:
            match digest:
                case "md5":
                    passwordHash = hashlib.md5(password.encode()).hexdigest()
                case "sha1":
                    passwordHash = hashlib.sha1(password.encode()).hexdigest()
                case "sha256":
                    passwordHash = hashlib.sha256(password.encode()).hexdigest()
                case "sha512":
                    passwordHash = hashlib.sha512(password.encode()).hexdigest()
            dictPasswords[passwordHash] = password
        
        
    #save the password dictionary to the local filesystem for later use
    print("Saved password dictionary as PasswordDictionary.txt")
    with open('PasswordDictionary.txt', 'w') as tempFile:
        tempFile.write(json.dumps(dictPasswords))
        
    return dictPasswords
    
#Look at the length of the hash and return what type of hash it is
def checkHashType (strHash):
    try:
        size = len(strHash)
        match size:
            case 32:
                return "md5"
            case 40:
                return "sha1"
            case 64:
                return "sha256"
            case 128:
                return "sha512"
            case _:
                print("Password Hash of {0} not recognized as a hash. Please ensure only the following hashes are used:\nmd5\nsha1\nsha256\nsha512".format(strHash))
                return None
    except:
        print("Hash provided must be in a string format")
        return None

#lookup the password in the dictionary based on the hash value passed to the script
def passwordLookup (passwordHash, passwordDictionary):    
    strHashType = checkHashType(passwordHash)
    if strHashType is not None:
        try:
            password = passwordDictionary[passwordHash]
            print("The corresponding password for the hash of {0} is:\n{1}".format(passwordHash, password))
        except:
            print("There is no corresponding password for the hash of {0}".format(passwordHash))



#Check the validity of the arguments to ensure they are correct before running the script
if args.passwordHash is None and args.passwordHashArray is None:
    print("passwordHash or passwordArray flags must be set for lookups to happen")
    parser.print_help()
    sys.exit(1)

if args.passwordHash is not None:
    if checkHashType(args.passwordHash) is None:
        parser.print_help()
        sys.exit(2)

if args.passwordHashArray is not None:
    incorrectHashes = []
    for passwordHash in args.passwordHashArray:
        if checkHashType(passwordHash) is None:
            incorrectHashes.append(passwordHash)
    if len(incorrectHashes) > 0:
        print("The following hashes are incorrect and not recognized by the script:\n")
        print(incorrectHashes)
        parser.print_help()
        sys.exit(3)


#Try to open the password dictionary or create one if none was specified as an argument
if args.passwordDictionary is None:
    print("No password dictionary was provided, creating it now")
    passwordDictionary = createPasswordDictionary()
else:
    try:
        #open the dictionary and check to make sure it's right
        with open(args.passwordDictionary, 'r') as tempFile:
            passwordDictionary = json.loads(tempFile.read())
        print("Loaded password dictionary of {0}".format(args.passwordDictionary))
    except:
        #exit with an issue
        print("The file with the password dictionary provided is not a json formatted file. Please ensure that you're using a json formatted file.")
        print("The file used was {0}".format(args.passwordDictionary))
        sys.exit(4)



#The body of the code that calls the lookups for the passwords
if args.passwordHash is not None:
    passwordLookup(args.passwordHash, passwordDictionary)
    
if args.passwordHashArray is not None:
    for passwordHash in args.passwordHashArray:
        passwordLookup(passwordHash, passwordDictionary)
