"""
This module house Trello object to:
1. Create a new Trello board
2. Add new members to the Trello board
"""

import argparse
import os
from loguru import logger
import requests

class Trello():
    "Trello Object to create boards and add members to the board"

    def __init__(self, key:str=None, token:str=None) -> None:
        """
        Initialize Trello class
        Parameters:
            key: Trello Key
            token: Trello Token
        Returns:
        """
        self.key = key
        self.token = token

    def create_board(self, board_name:str) -> str: # pylint: disable=inconsistent-return-statements
        """
        Create a new board on Trello
        Parameters:
            board_name: New Trello board name
        Returns:
            board_id: Board ID for the new Trello board
        """
        params = {'key':self.key, 'token':self.token, 'name':board_name}
        url = 'https://api.trello.com/1/boards/'
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created Board - {board_name}")
            board_id = response.json()['id']
            return board_id
        except Exception as create_board_err: # pylint: disable=broad-except
            logger.exception("Unable to create new Board")
            logger.exception(str(create_board_err))

    def add_members_to_board(self, board_id:str, members:list) -> None:
        """
        Add members to a Board
        Parameters:
            board_id: Board ID of the newly created board
            members: List of members
        Returns:
        """
        for account in members:
            params = {'key':self.key, 'token':self.token}
            try:
                #Get the member ID using email ID
                get_member_id = requests.get(url=f"https://api.trello.com/1/members/{account}",
                                             params=params)
                if get_member_id.status_code == 200:
                    logger.success(f"Successfully attained member ID for {account}")
                else:
                    logger.error(f"Failed to attain member ID for {account}")
                    continue
                member_id = get_member_id.json()['id']

                # Add member to the board
                url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
                params = {'key':self.key, 'token':self.token, 'type':'normal'}
                response = requests.put(url=url, params=params)
                response.raise_for_status()
                logger.success(f"Sucessfully added {account} to new board")
            except Exception as add_member_err: # pylint: disable=broad-except
                logger.exception(f"Unable to add member - {account}")
                logger.exception(str(add_member_err))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--create",
                        dest='create',
                        action='store_true',
                        default=False,
                        help='--create will create a new board')
    parser.add_argument("--board_name",
                        dest="board_name",
                        help="Enter the board name",
                        default="Test Board")
    args = parser.parse_args()

	# Get the key, token, members & board_name from env
    TRELLO_KEY = os.environ.get("TRELLO_KEY")
    TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")
    TRELLO_MEMBERS = os.environ.get("TRELLO_MEMBERS") # should be a comma seperated value
    TRELLO_MEMBERS = TRELLO_MEMBERS.split(',')
    #TRELLO_BOARD_NAME = "Test Board"

    if args.create:
        trello_obj = Trello(key=TRELLO_KEY, token=TRELLO_TOKEN)
        # Create board
        new_board_id = trello_obj.create_board(args.board_name)
        # Add members to board
        trello_obj.add_members_to_board(new_board_id, TRELLO_MEMBERS)
    else:
        parser.print_usage()
