---------------------
Create Trello Boards
---------------------

You can use this script to create Trello Boards and add members to it

-----
Setup
-----

The setup has two parts:

1. Prerequisites  
2. Create a configuration file

__1. Prerequisites__

a) Install Python 3.x

b) Add Python 3.x to your PATH environment variable

c) If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)

d) pip install -r requirements.txt to install dependencies

__2. Create a configuration file__

Create a conf.py file and add the following paramters

a) key - App key from https://trello.com/app-key

b) token - Token generated from a redirect in previous step 

c) board_name - The name of the Board to be created

d) members - The members list needed to be added to the Board

Sample values inside a conf.py file

key = '<your_key>'

token = '<yout_token>'

board_name = '<board_name>'

members = []

-----
How to run
-----

python3 ./trello.py --create





