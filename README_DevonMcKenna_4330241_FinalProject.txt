Devon McKenna
#4330241
CS3130 - Final Project

To Run Server:     python3 Hangman.py server ''
To Run Client:     ptyhon3 Hangman.py client ''
---------------------------------------------------------------------------------------

Final Project (multi)client-(single)server version of 'Hangman'.

Once the server has been started, multiple clients may connect and communicate with it through select commands.

Commands:
    help:                   lists accepted commands and gives instructions on how to play the game
    exit:                   closes the client


The server will find a random word from it's database (text file) and set it to the client.  It will then interact with the client, sending relevant information to it as well as accepting input.

Pretty basic game but it's still fun.



The code handles basic exceptions.  Checks if inputs are acceptable (aka. letters or commands) or if any problems occur from opening files.



----------------------------------------------------------------------------------------


On GitHub:

    https://github.com/mckennad/FinalProject.git
