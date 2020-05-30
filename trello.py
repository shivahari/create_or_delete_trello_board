#! /usr/bin/python3

import conf #conf file for Trello
import requests
import json
import argparse
import os
from loguru import logger

class Trello(object):
    "Trello Class to create/delete boards and add members to the board"
    
    def __init__(self):
        "Initialize Trello class"
        try:
            self.key = conf.key
            self.token = conf.token
            self.board_name = conf.board_name
            self.members = conf.members
            self.new_board_id = None
        except Exception as e:
            logger.critical("Unable to read from conf file.\n Please make sure you have a conf.py file with \
                    \n1. key - App key from https://trello.com/app-key \
                    \n2. token - Token from https://trello.com/1/token/approve \
                    \n3. board_name - The name of the Board to be created  \
                    \n4. members - The members needed to be added to the Board")
        #Create a log dir
        try:
            if not os.path.exists('./log'):
                os.mkdir('log')
            logger.add('./log/file-{time}.log',format='{name} {message}',rotation='5 MB')
        except Exception as e:
            logger.critical(str(e))

    def get_boards(self):
        "Get the Boards associated with the user"
        all_boards = None
        params = {'key':self.key,'token':self.token,'fields':'name'}
        url = 'https://api.trello.com/1/members/me/boards'
        try:
            response = requests.get(url=url,params=params)
            result_flag = True if response.status_code == 200 else False
            self.log_result(result_flag,"Successfully Obtained Board names","Failed to get the Board names")
            if result_flag:
                all_boards = response.json()
        except Exception as e:
            logger.exception("Unable to Get the Boards")
            logger.exception(str(e))
        finally:
            return all_boards
    
    def create_board(self):
        "Create a new board on Trello"
        if self.board_name:
            params = {'key':self.key,'token':self.token,'name':self.board_name}
            url = 'https://api.trello.com/1/boards/'
            try:
                response = requests.post(url=url,params=params)
                result_flag = True if response.status_code == 200 else False
                self.log_result(result_flag,"Successfully created Board - %s"%self.board_name,"Failed to create new Board")
                if result_flag:
                    self.new_board_id = response.json()['id']
                self.add_members()
            except Exception as e:
                logger.exception("Unable to create new Board")
                logger.exception(str(e))
   
    def add_members(self):
        "Add members to a Board"
        if self.new_board_id:
            for account in self.members:
                params = {'key':self.key,'token':self.token}
                try:
                    #Get the member ID using email ID
                    get_member_id = requests.get(url='https://api.trello.com/1/members/%s'%account,params=params)
                    result_flag = True if get_member_id.status_code == 200 else False
                    self.log_result(result_flag,"Successfully attained member ID for %s"%account,"Failed to get member ID for %s"%account)
                    member_id = None
                    if get_member_id.status_code == 200:
                        member_id = get_member_id.json()['id']
                    if member_id:
                        url = 'https://api.trello.com/1/boards/%s/members/%s'%(self.new_board_id,member_id)
                        params = {'key':self.key,'token':self.token,'type':'normal'}
                        response = requests.put(url=url,params=params)
                        result_flag = True if response.status_code == 200 else False
                        self.log_result(result_flag,"Sucessfully added %s to Board %s"%(account,self.board_name),"Failed to add %s to Board %s"%(account,self.board_name))
                except Exception as e:
                    logger.exception("Unable to add member - %s"%account)
                    logger.exception(str(e))

    def log_result(self,result_flag,success_msg,failure_msg):
        "Log results using loguru"
        if result_flag:
            logger.success(success_msg)
        else:
            logger.error(failure_msg)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--create",dest='create',action='store_true',default=False,help='--create will create a new board')
    args = parser.parse_args()
    if args.create:
        try:
            trello_obj = Trello()
            trello_obj.create_board()
        except Exception as e:
            logger.critical(str(e))
    else:
        parser.print_usage()
            

        
