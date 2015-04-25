import re, sys, argparse, random, socket


MAX_BYTES = 65535

#---------------------------------------------------



def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print ('Listening at ', sock.getsockname())


    while True:


        data, address = sock.recvfrom(MAX_BYTES);
        #print(address)          #debuggin with print

        text = data.decode('ascii')

        if(text == "help"):         #help
            message = HMHelp()

        elif (text == "This is another message"):   #Need to grab word and setup user!!    
            message = newPlayer(address[1])

        elif(text == "exit"):         #exit protocol
            message = HMExit(address[1])

        elif(len(text) == 1):
            message = "> Program only accepts lower-case alphabetical characters"
            if(text.isalpha()):
                if(text.islower()):
                    message = playerExists(text, address[1])

        else:
            message = "> Not a command.  Try entering \"help\" for assistance\n"

        
        sock.sendto(message.encode('ascii'), address)



#---------------------------------------------------



def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))

    delay = 0.1 # seconds
    text = 'This is another message'
    data = text.encode('ascii')


    while True:
        sock.send(data)
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc:
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
        else:
            message = data.decode('ascii')
            breakAndprint(message)
            break # we are done, and can stop looping



    while True:
        print("\nGuess a letter: ", end = "")
        text = input()
        print()
        data = text.encode('ascii')

        sock.send(data)
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc:
            delay *= 2 # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
        else:
            response = data.decode('ascii')
            breakAndprint(response)

            if(response[0] == '#'):
                break # we are done, and can stop looping
            elif (response[0] == '@'):
                break


#---------------------------------------------------



def HMHelp():
#send back help information to server to be printed to the user

    return ">\n Each \'_\' indicates a letter that you need to guess.\n Enter one letter (lower-case) at a time and try to complete the word.\n You fail if you guess wrong 6 times.\n You can type \"exit\" to end the program.\n\n"


#---------------------------------------------------



def newPlayer(port):
#sets up new user with port number, random word chosen from file, "_" for length of line to track discover, letters correctly previously guesses, and starts wrong-guess count at 0 (places this info in file for later use

    words = []
    players = {}
    userInfo = ""

    try:
        infile = open("HangmanWords.txt","r")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message


    for line in infile:
        words.append((line.rstrip("\n")))
    infile.close()

    ranNum = random.randint(0, (len(words)-1))


    try:
        infile = open("HangmanUsers.txt","a")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message



    userInfo = str(port) + ":" + words[ranNum] + ":" + "_ "*len(words[ranNum]) +":" + ":0\n"
    infile.writelines(userInfo)

    #mess ="\n" + "_"*len(words[ranNum])   REMOVED AND SENDING userInfo INSTEAD

    return userInfo



#---------------------------------------------------



def playerExists(text, port):
#Identifies user, splits up data and compares text.  Modifies data where needed and returns info to player

    word = ""
    users = {}
    correct = False
    usersP2 = {}
    mess = ""


    try:
        infile = open("HangmanUsers.txt","r")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message


    for line in infile:
        ID, info = line.split(":",1)
        users[ID] = info
    infile.close()


    for ID in users:
        if(str(port) == ID):
            word, rest = users[ID].split(":",1)     #suppose I could have just split more than once here, meh
            incWord, letters, rest2 = rest.split(":",2)

            addToLetters = True
            for ch in letters:
                if(ch == text):
                    addToLetters = False
            if(addToLetters):
                letters += text

            incWord = ""
            for char in word:
                if(text == char):
                    correct = True

            for char in word:
                charMissing = True
                for ch in letters:
                    if(ch == char):
                        incWord += ch
                        charMissing = False
                if(charMissing):
                    incWord += "_ "
                

            if(correct):
                users[ID] = word + ":" + incWord + ":" +letters + ":" + rest2

                try:
                    infile = open("HangmanUsers.txt","w")
                except IOError as err:
                    errno, strerror = err.args
                    print("I/O error({0}): {1}".format(errno, strerror))
                    sys.exit()
                    #detects open error and outputs error code and message
                except FileNotFoundError as err:
                    errno, strerror = err.args
                    print("FileNotFoundError error({0}): {1}".format(errno, strerror))
                    sys.exit()
                    #detects open error and outputs error code and message
                except NameError as err:
                    errno, strerror = err.args
                    print("NameError error({0}): {1}".format(errno, strerror))
                    sys.exit()
                    #detects open error and outputs error code and message


                wordComplete = True
                for char in incWord:
                    if("_" == char):
                        wordComplete = False

                if(wordComplete):

                    for ID in users:                                #updates Users file (removes this user from list)
                        if(ID != str(port)):
                            newLine = [ID,":",users[ID]]
                            infile.writelines(newLine)
                    infile.close()

                    mess = "#" + ID + ":" + users[ID] + "$\nCongratulations!!!   You win!\n\n--\n"
                    return mess

                else:

                    for ID in users:                                #updates Users file (wCount and incWord)
                        newLine = [ID,":",users[ID]]
                        infile.writelines(newLine)
                    infile.close()
                    
                    mess = ID + ":" + users[ID]
                    return mess

            


            else:
                rest3 = rest2.rstrip("\n")
                wCount = int(rest3) + 1
                rest2 = str(wCount) + "\n"
                users[ID] = word + ":" + incWord + ":" + letters + ":" + rest2

                if(wCount < 6):
                    
                    try:
                        infile = open("HangmanUsers.txt","w")
                    except IOError as err:
                        errno, strerror = err.args
                        print("I/O error({0}): {1}".format(errno, strerror))
                        sys.exit()
                        #detects open error and outputs error code and message
                    except FileNotFoundError as err:
                        errno, strerror = err.args
                        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
                        sys.exit()
                        #detects open error and outputs error code and message
                    except NameError as err:
                        errno, strerror = err.args
                        print("NameError error({0}): {1}".format(errno, strerror))
                        sys.exit()
                        #detects open error and outputs error code and message

                    for ID in users:                                #updates Users file
                        newLine = [ID,":",users[ID]]
                        infile.writelines(newLine)
                    infile.close()

                    mess = ID + ":" + users[ID]
                    return mess

                else:

                    try:
                        infile = open("HangmanUsers.txt","w")
                    except IOError as err:
                        errno, strerror = err.args
                        print("I/O error({0}): {1}".format(errno, strerror))
                        sys.exit()
                        #detects open error and outputs error code and message
                    except FileNotFoundError as err:
                        errno, strerror = err.args
                        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
                        sys.exit()
                        #detects open error and outputs error code and message
                    except NameError as err:
                        errno, strerror = err.args
                        print("NameError error({0}): {1}".format(errno, strerror))
                        sys.exit()
                        #detects open error and outputs error code and message

                    for ID in users:
                        if(str(port) != ID):
                            newLine = [ID,":",users[ID]]
                            infile.writelines(newLine)
                    infile.close()

                    mess = "#" + ID + ":" + users[ID] + "$\n Sorry, you lose.\n Thanks for playing!\n\n--\n"
                    return mess
           

    return "@Uh oh\n\n--\n"


#---------------------------------------------------



def breakAndprint(message):
#client-method that breaks down return message from server, determines which picture to grab from Art, and prints out all client side info

    if(message[0] == '@'):
        print(message[1:])          #Unfortunately, while this is rare, it could lead to problems later down the road due to improper exit leaving port number in HangmanUsers.txt

    elif(message[0] == '>'):
        print(message[1:])

    elif(message[0] == '#'):

        garbage, mess = message.rsplit("$")
        garbage = garbage[1:]

        if(mess == "\n Sorry, you lose.\n Thanks for playing!\n\n--\n"):

            try:
                infile = open("HangmanArt6.txt","r")
            except IOError as err:
                errno, strerror = err.args
                print("I/O error({0}): {1}".format(errno, strerror))
                sys.exit()
                #detects open error and outputs error code and message
            except FileNotFoundError as err:
                errno, strerror = err.args
                print("FileNotFoundError error({0}): {1}".format(errno, strerror))
                sys.exit()
                #detects open error and outputs error code and message
            except NameError as err:
                errno, strerror = err.args
                print("NameError error({0}): {1}".format(errno, strerror))
                sys.exit()
                #detects open error and outputs error code and message

            for line in infile:
                print(line)
            infile.close()

            ID, garbage2 = garbage.split(":",1)
            Word, garbage3 = garbage2.split(":",1)
            print("\n\n" + Word + "\n")
            print(mess)


        else:
            garbage2 = garbage.rstrip("\n")
            garbage3, wCount = garbage2.rsplit(":",1)

            fileToOpen = "HangmanArt6.txt"

            if(int(wCount) == 0):                   #used to determine which art file needs to be opened (thought better of having them all in one txt file and searching through it)
                fileToOpen = "HangmanArt0.txt"
            elif(int(wCount) == 1):
                fileToOpen = "HangmanArt1.txt"
            elif(int(wCount) == 2):
                fileToOpen = "HangmanArt2.txt"
            elif(int(wCount) == 3):
                fileToOpen = "HangmanArt3.txt"
            elif(int(wCount) == 4):
                fileToOpen = "HangmanArt4.txt"
            elif(int(wCount) == 5):
                fileToOpen = "HangmanArt5.txt"
            elif(int(wCount) == 6):
                fileToOpen = "HangmanArt6.txt"

            try:
                infile = open(fileToOpen,"r")
            except IOError as err:
                errno, strerror = err.args
                print("I/O error({0}): {1}".format(errno, strerror))
                sys.exit()
                #detects open error and outputs error code and message
            except FileNotFoundError as err:
                errno, strerror = err.args
                print("FileNotFoundError error({0}): {1}".format(errno, strerror))
                sys.exit()
                #detects open error and outputs error code and message
            except NameError as err:
                errno, strerror = err.args
                print("NameError error({0}): {1}".format(errno, strerror))
                sys.exit()
                #detects open error and outputs error code and message

            for line in infile:
                print(line)
            infile.close()

            garbage4, compWord, letters = garbage3.rsplit(":",2)
            print("\n\n" + compWord + "\n")
            print(mess)

    else:

        port, Word, incWord, letters, wCount = message.split(":")        #breaks apart passed message
        wCount = wCount.rstrip("\n")

        fileToOpen = "HangmanArt6.txt"

        if(int(wCount) == 0):
            fileToOpen = "HangmanArt0.txt"
        elif(int(wCount) == 1):
            fileToOpen = "HangmanArt1.txt"
        elif(int(wCount) == 2):
            fileToOpen = "HangmanArt2.txt"
        elif(int(wCount) == 3):
            fileToOpen = "HangmanArt3.txt"
        elif(int(wCount) == 4):
            fileToOpen = "HangmanArt4.txt"
        elif(int(wCount) == 5):
            fileToOpen = "HangmanArt5.txt"
        elif(int(wCount) == 6):
            fileToOpen = "HangmanArt6.txt"

        try:
            infile = open(fileToOpen,"r")
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))
            sys.exit()
            #detects open error and outputs error code and message
        except FileNotFoundError as err:
            errno, strerror = err.args
            print("FileNotFoundError error({0}): {1}".format(errno, strerror))
            sys.exit()
            #detects open error and outputs error code and message
        except NameError as err:
            errno, strerror = err.args
            print("NameError error({0}): {1}".format(errno, strerror))
            sys.exit()
            #detects open error and outputs error code and message
        
        for line in infile:
            print(line)
        infile.close()

        print(incWord)

        
        
            


#---------------------------------------------------



def HMExit(port):
#checks if user address (port only since all our clients share IP) matches a user currently marked as "online", if so, modify data and notify of logout.

    users = {}

    try:
        infile = open("HangmanUsers.txt","r")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message

    for line in infile:
        ID, info = line.split(":",1)
        users[ID] = info
    infile.close()


    try:
        infile = open("HangmanUsers.txt","w")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message


    for ID in users:
        if(str(port) != ID):
            newLine = [ID, ":", users[ID]]
            infile.writelines(newLine)
    infile.close()

    

    return "@ Thanks for playing!\n\n--\n"



#---------------------------------------------------


#copy-pasted from "udp_remote.py" and makes me a little dizzy looking at it.  O.o


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,' ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;' ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

