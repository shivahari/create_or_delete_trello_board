---------------------
Create Trello Boards
---------------------

You can use this script to create Trello Boards and add members to it

-----
Setup
-----

The setup has two parts:
1. Prerequisites  
2. Create Env variables

__1. Prerequisites__
a) Install Python 3.x

b) Add Python 3.x to your PATH environment variable

c) If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)

d) `pip install -r requirements.txt` to install dependencies

__2. Create Env variables__
Create the following Env variables

a) TRELLO_KEY - App key from https://trello.com/app-key

b) TRELLO_TOKEN - Token generated from a redirect in previous step 

c) TRELLO_MEMBERS - The members list needed to be added to the Board

-----
How to run
-----

python3 ./trello.py --create
