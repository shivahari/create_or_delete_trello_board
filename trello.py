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

    def create_card(self, list_id:str, card_name:str, **kwargs) -> str: # pylint: disable=inconsistent-return-statements
        """
        Create a new card on Trello baord
        Parameters:
            card_name: New Trello card name
        Returns:
            card-id: Card ID for the new Trello card
        """
        params = {'key':self.key, 'token':self.token, 'name':card_name, 'idList':list_id}
        params.update(kwargs)  # Add any additional params from kwargs
        url = 'https://api.trello.com/1/cards/'
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created Board - {card_name}")
            card_id = response.json()['id']
            return card_id
        except Exception as create_card_err: # pylint: disable=broad-except
            logger.exception("Unable to create new Board")
            logger.exception(str(create_card_err))

    def create_list(self, board_id:str, list_name:str, **kwargs) -> str: # pylint: disable=inconsistent-return-statements
        """
        Create a new list on Trello board
        Parameters:
            list_name: New Trello board List name
        Returns:
            list_id: List ID for the new Trello board List
        """
        params = {'key':self.key, 'token':self.token, 'name':list_name, 'idBoard':board_id }
        params.update(kwargs)  # Add any additional params from kwargs
        url = 'https://api.trello.com/1/lists/'
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created list - {list_name}")
            list_id = response.json()['id']
            return list_id
        except Exception as create_list_err: # pylint: disable=broad-except
            logger.exception("Unable to create todo list")
            logger.exception(str(create_list_err))

    def create_checklist(self, card_id:str, checklist_name:str, **kwargs) -> str: # pylint: disable=inconsistent-return-statements
        """
        Create a new checklist on Trello card
        Parameters:
            checklist_name: New checklist name
        Returns:
            checklist_id: Checklist ID for the new card checklist
        """
        params = {'key':self.key, 'token':self.token, 'name':checklist_name }
        params.update(kwargs)  # Add any additional params from kwargs
        url = f'https://api.trello.com/1/cards/{card_id}/checklists'
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created list - {checklist_name}")
            checklist_id = response.json()['id']
            return checklist_id
        except Exception as create_checklist_err: # pylint: disable=broad-except
            logger.exception("Unable to create todo list")
            logger.exception(str(create_checklist_err))

    def add_checkitem(self, card_id:str, checklist_id:str, **kwargs) -> str: # pylint: disable=inconsistent-return-statements
        """
        Create a new checklist on Trello card
        Parameters:
            checklist_name: New checklist item name
        Returns:
            checklist_item_id: Checklist Item ID for the new checklist items
        """
        params = {'key':self.key, 'token':self.token}
        params.update(kwargs)  # Add any additional params from kwargs
        url = f'https://trello.com/1/cards/{card_id}/checklist/{checklist_id}/checkItem'
        checklist_item_name = kwargs.get('name', 'Unnamed Item')
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully added checklist item: {checklist_item_name}")
            checklist_item_id = response.json()['id']
            return checklist_item_id
        except Exception as create_checklist_item_err: # pylint: disable=broad-except
            logger.exception("Unable to create todo list")
            logger.exception(str(create_checklist_item_err))

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
    TRELLO_BOARD_NAME = "Test Board"
    TODO_LIST_NAME = "TO DO"
    DONE_LIST_NAME = "Done"
    RETROSPECTIVE_CARD_NAME = "Retrospective"
    NEWSLETTER_INCHARGE_CARD_NAME = "Newsletter Incharge"
    NEWSLETTER_DESCRIPTION = (
        "From 14th Oct 2024 we will have everyone pick articles for newsletter. Each person assigned will need to "
        "identify articles and finish updating description by Wednesday afternoon. The person in charge to send newsletter, "
        "needs to create the campaign, login to mailchimp, test and schedule the newsletter.\n\n"
        "Newsletter assignee master sheet: https://docs.google.com/spreadsheets/d/1cxn39Q6uEr7USS3t-AU6yFUDRhwPe3NE98XgXefQuXs/edit?usp=sharing"
    )
    RETROSPECTIVE_CARD_NAME = "Retrospective"
    RETROSPECTIVE_DESCRIPTION = "We use this card to note down good/bad/change that happened this week."
    CHECKLIST_NAME = "Non-Sprint Activities"
    SURVEY= "Survey"
    HIRING = "Hiring"
    CLIENT_UPDATES = "Client Updates"
    ANYTHING_ELSE = "Anything else?"
    if args.create:
        trello_obj = Trello(key=TRELLO_KEY, token=TRELLO_TOKEN)
        # Create board
        new_board_id = trello_obj.create_board(args.board_name)
        # Add members to board
        trello_obj.add_members_to_board(new_board_id, TRELLO_MEMBERS)
        # Create a To Do list
        todo_list_id = trello_obj.create_list(new_board_id, TODO_LIST_NAME)
        # Create a Done list
        done_list_id = trello_obj.create_list(new_board_id, DONE_LIST_NAME, pos='bottom')
        # Add Newsletter Incharge card in the To Do list
        newsletter_card_id = trello_obj.create_card(todo_list_id, NEWSLETTER_INCHARGE_CARD_NAME, desc=NEWSLETTER_DESCRIPTION)
        # Add Retrospective card in the To Do list
        retrospective_card_id = trello_obj.create_card(todo_list_id, RETROSPECTIVE_CARD_NAME, desc=RETROSPECTIVE_DESCRIPTION, pos='top')
        # Create a checklist in retrospective card
        checklist_id = trello_obj.create_checklist(retrospective_card_id, CHECKLIST_NAME)
        # Add Non sprint activity checklist items
        survey_check_id = trello_obj.add_checkitem(retrospective_card_id, checklist_id, name=SURVEY)
        hiring_check_id = trello_obj.add_checkitem(retrospective_card_id, checklist_id, name=HIRING)
        client_update_check_id = trello_obj.add_checkitem(retrospective_card_id, checklist_id, name=CLIENT_UPDATES)
        anything_else_check_id = trello_obj.add_checkitem(retrospective_card_id, checklist_id, name=ANYTHING_ELSE)
    else:
        parser.print_usage()
