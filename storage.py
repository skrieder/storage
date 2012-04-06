import os
import sys

bucketName = 'skrieder'
# declare the insert
def Insert(key, value):
    try:
        insertCMD = 'gsutil cp '+ sys.argv[2] + ' ' + 'gs://' + bucketName
        os.system(insertCMD)
        return True
    except:
        return False

# declare the delete
def Remove(key):
    try:
        removeCMD = 'gsutil rm gs://'+ bucketName + '/' + sys.argv[2]
        os.system(removeCMD)
        return True
    except:
        return False

#define listing
def Listing(key):
    try:
        #declare bucketname
        bN = key
        #declare constant for gs://
        pre = 6
        # write the output file
        checkCMD = 'gsutil ls gs://' + bucketName + '/ > ~/Desktop/storage/output.txt'
        os.system(checkCMD)
        # declare the array
        array2 = []
        ins2 = open( "output.txt", "r" )
        for line2 in ins2:
            line2 = line2[len(bN)+pre:len(line2)-1]
            array2.append(line2)
        #print(array2)
        return(array2)
    except:
        print("Error, exception thrown in Listing()")
        return False

# declare the check
def Check(key):
    try:
        CheckArray = []
        CheckArray = Listing(bucketName)
        KeyToCheck = sys.argv[2]
        if KeyToCheck in CheckArray:
            # print("Key Found!")
            return True
        else:
            # print("Key Not Found!")
            return False
    except:
        return False

# declare the find
def Find(key):
    if Check(key) == True:
        os.system('gsutil cp gs://' + bucketName + '/' + key + ' ~/Desktop/storage/')
        str3 = ""
        ins3 = open( key, "r" )
        for line3 in ins3:
            str3 += line3
        #print(str3)
        return(str3)
    else:
        print("File Not Found!")
        return False

# declare the manual
def manual():
    print("Welcome to Python Storage")
    print("The following commands are available:")
    print("Insert:")

###main program###
if(len(sys.argv) > 1):
    if(sys.argv[1] == 'insert'):
        Insert(sys.argv[2], sys.argv[2])
    elif(sys.argv[1] == 'remove'):
        if(len(sys.argv) > 2):
            Remove(sys.argv[2])
    elif(sys.argv[1] == 'check'):
        if(len(sys.argv) > 2):
            Check(sys.argv[2])
    elif(sys.argv[1] == 'listing'):
        if(len(sys.argv) > 2):
            Listing(sys.argv[2])
    elif(sys.argv[1] == 'find'):
        if(len(sys.argv) > 2):
            Find(sys.argv[2])
    elif(sys.argv[1] == 'help'):
        manual()
else:
    print('python storage.py "command"')
    print('type python storage.py help for the manual')


