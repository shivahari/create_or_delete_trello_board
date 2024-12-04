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

    def _get_params(self, **kwargs):
        """Build common parameters for API requests."""
        params = {'key': self.key, 'token': self.token}
        params.update(kwargs)
        return params

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

    def add_members_to_board(self, board_id: str, members: list) -> None:
        """
        Add members to a Board
        Parameters:
            board_id: Board ID of the newly created board
            members: List of members
        Returns:
        """
        for account in members:
            params = {"key": self.key, "token": self.token}
            try:
                # Get the member ID using email ID
                get_member_id = requests.get(
                    url=f"https://api.trello.com/1/members/{account}", params=params
                )
                if get_member_id.status_code == 200:
                    logger.success(f"Successfully attained member ID for {account}")
                else:
                    logger.error(f"Failed to attain member ID for {account}")
                    continue
                member_id = get_member_id.json()["id"]

                # Add member to the board
                url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
                params = {"key": self.key, "token": self.token, "type": "normal"}
                response = requests.put(url=url, params=params)
                response.raise_for_status()
                logger.success(f"Sucessfully added {account} to new board")
            except Exception as add_member_err:  # pylint: disable=broad-except
                logger.exception(f"Unable to add member - {account}")
                logger.exception(str(add_member_err))

    def create_card(self, list_id: str, card_name: str, **kwargs) -> str:
        """
        Create a new card on Trello baord
        Parameters:
            card_name: New Trello card name
        Returns:
            card-id: Card ID for the new Trello card
        """
        url = "https://api.trello.com/1/cards/"
        params = self._get_params(name=card_name, idList=list_id, **kwargs)
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created Board - {card_name}")
            return response.json()["id"]
        except requests.exceptions.HTTPError as error:
            logger.error(f"Unable to create new card: {error}")
            return None

    def create_list(self, board_id: str, list_name: str, **kwargs) -> str:
        """
        Create a new list on Trello board
        Parameters:
            list_name: New Trello board List name
        Returns:
            list_id: List ID for the new Trello board List
        """
        url = "https://api.trello.com/1/lists/"
        params = self._get_params(name=list_name, idBoard=board_id, **kwargs)
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created list - {list_name}")
            return response.json()["id"]
        except requests.exceptions.HTTPError as error:
            logger.error(f"Unable to create list: {error}")
            return None

    def create_checklist(self, card_id: str, checklist_name: str, **kwargs) -> str:
        """
        Create a new checklist on Trello card
        Parameters:
            checklist_name: New checklist name
        Returns:
            checklist_id: Checklist ID for the new card checklist
        """
        url = f"https://api.trello.com/1/cards/{card_id}/checklists"
        params = self._get_params(name=checklist_name, **kwargs)
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully created list - {checklist_name}")
            return response.json()["id"]
        except requests.exceptions.HTTPError as error:
            logger.error(f"Unable to create checklist: {error}")
            return None

    def add_checkitem(
        self, card_id: str, target_checklist_id: str, **kwargs
    ) -> str:
        """
        Create a new checklist on Trello card
        Parameters:
            checklist_name: New checklist item name
        Returns:
            checklist_item_id: Checklist Item ID for the new checklist items
        """
        url = f"https://trello.com/1/cards/{card_id}/checklist/{target_checklist_id}/checkItem"
        params = self._get_params(**kwargs)
        checklist_item_name = kwargs.get("name", "Unnamed Item")
        try:
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            logger.success(f"Successfully added checklist item: {checklist_item_name}")
            return response.json()["id"]
        except requests.exceptions.HTTPError as error:
            logger.error(f"Unable to add checklist item: {error}")
            return None


def define_retro_data():
    """
    Define the data for the Retrospective card
    """
    return {
        "TODO_LIST_NAME": "TO DO",
        "DONE_LIST_NAME": "Done",
        "RETROSPECTIVE_CARD_NAME": "Retrospective",
        "NEWSLETTER_INCHARGE_CARD_NAME": "Newsletter Incharge",
        "NEWSLETTER_DESCRIPTION": (
            """From 14th Oct 2024 we will have everyone pick articles for the newsletter.
            Each person assigned will need to identify articles and finish updating description 
            by Wednesday afternoon. The person in charge to send newsletter, needs to create the 
            campaign, login to Mailchimp, test, and schedule the newsletter.

            Newsletter assignee master sheet: 
            https://docs.google.com/spreadsheets/d/1cxn39Q6uEr7USS3t-AU6yFUDRhwPe3NE98XgXefQuXs/edit?usp=sharing"""
        ),
        "RETROSPECTIVE_DESCRIPTION": "We use this card to note down good/bad/change that happened this week.",
        "CHECKLIST_NAME": "Non-Sprint Activities",
        "SURVEY": "Survey",
        "HIRING": "Hiring",
        "CLIENT_UPDATES": "Client Updates",
        "ANYTHING_ELSE": "Anything else?",
    }


if __name__ == "__main__":
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
    TRELLO_MEMBERS = os.environ.get(
        "TRELLO_MEMBERS"
    )  # should be a comma seperated value
    TRELLO_MEMBERS = TRELLO_MEMBERS.split(",")
    TRELLO_BOARD_NAME = "Test Board"

    retro_data = define_retro_data()

    if args.create:
        trello_obj = Trello(key=TRELLO_KEY, token=TRELLO_TOKEN)
        # Create board
        new_board_id = trello_obj.create_board(args.board_name)
        # Add members to board
        trello_obj.add_members_to_board(new_board_id, TRELLO_MEMBERS)
        # Create a To Do list
        todo_list_id = trello_obj.create_list(
            new_board_id, retro_data["TODO_LIST_NAME"]
        )
        trello_obj.create_list(new_board_id, retro_data["DONE_LIST_NAME"], pos="bottom")
        trello_obj.create_card(
            todo_list_id,
            retro_data["NEWSLETTER_INCHARGE_CARD_NAME"],
            desc=retro_data["NEWSLETTER_DESCRIPTION"],
        )
        retrospective_card_id = trello_obj.create_card(
            todo_list_id,
            retro_data["RETROSPECTIVE_CARD_NAME"],
            desc=retro_data["RETROSPECTIVE_DESCRIPTION"],
            pos="top",
        )
        checklist_id = trello_obj.create_checklist(
            retrospective_card_id, retro_data["CHECKLIST_NAME"]
        )
        trello_obj.add_checkitem(
            retrospective_card_id, checklist_id, name=retro_data["SURVEY"]
        )
        trello_obj.add_checkitem(
            retrospective_card_id, checklist_id, name=retro_data["HIRING"]
        )
        trello_obj.add_checkitem(
            retrospective_card_id, checklist_id, name=retro_data["CLIENT_UPDATES"]
        )
        trello_obj.add_checkitem(
            retrospective_card_id, checklist_id, name=retro_data["ANYTHING_ELSE"]
        )
    else:
        parser.print_usage()
