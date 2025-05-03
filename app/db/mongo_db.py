from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import uuid
import time
import logging
import pymongo

from app.config import DATABASE_CONFIG
from app.schema import UserInfoSchema
from app.logger import Logger

db_config = DATABASE_CONFIG["mongo"]
logger = Logger("mongo", log_level=logging.DEBUG)

class MongoDB:
    """
    A class to handle MongoDB operations for storing and retrieving AI conversation data.
    """

    def __init__(self):
        """
        Initialize MongoDB connection.
        
        Args:
            collection_name (str): Collection name for storing conversations
        """
        self.client = MongoClient(db_config["uri"])
        self.db = self.client[db_config["name"]]
        self.chat_history_table = self.db[db_config["chat_history_table"]]
        self.user_table = self.db[db_config["user_table"]]
        self.conversation_table = self.db[db_config["conversation_table"]]

        self.status()
    
    def status(self):
        try:
            self.client.server_info()  
            logger.info("MongoDB connect successfully!")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logger.error("MongoDB connection error: ", err)   

    def reset(self):
        self.client[self.db][self.user_table].drop()
        self.client[self.db][self.chat_history_table].drop()
    
    def add_user(self, user_id, user_info: UserInfoSchema):
        if self.user_table.find_one({'id' : user_id}):
            logger.warning(f"Add info user {user_id} failed: user_id existed")
            return None
        cursor = self.user_table.insert_one(
            {
                "id": user_id,
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
                **user_info.__dict__ 
            }
        )
        logger.info(f"Add info user {user_id} success")
        return cursor
    
    def query_user_by_id(self, user_id):
        user_info = self.user_table.find_one({'id' : user_id})
        if user_info:
            logger.info(f"Query user {user_id} success")
            return UserInfoSchema(**user_info)
        else:
            logger.warning(f"Query user {user_id} fail: user_id not existed")
            return None
    
    def update_user(self, user_id, user_info: UserInfoSchema):
        user_info_dict = user_info.__dict__
        user_info_dict["updated_at"] = int(time.time())

        if self.user_table.find_one({'id' : user_id}):
            self.user_table.update_one({'id' : user_id}, {'$set': user_info_dict})
            logger.info(f"Update user {user_id} success")
        else:
            logger.warning(f"Update user {user_id} fail: user_id not existed")

    def init_conversation(self, user_id):
        conversation_id = str(uuid.uuid4())
        
        self.conversation_table.insert_one({
            "id": conversation_id,
            "user_id": user_id,
            "activate": True,
            "created_at": int(time.time())
        })
        logger.info(f"User {user_id} init conversation {conversation_id} success")
        return conversation_id
    
    def unactivate_conversation_id(self, conversation_id):
        self.conversation_table.update_one(
            {"id": conversation_id},
            {"$set": {"activate": False}}
        )
        logger.info(f"Conversation {conversation_id} unactivate success")

    def get_conversation_ids_from_user_id(self, user_id, sort_latest=True):
        cursor = self.conversation_table.find({'user_id' : user_id})
        if sort_latest:
            cursor.sort("created_at", DESCENDING)
        
        conversation_ids = []
        for conversation_id in cursor:
            if not conversation_id["activate"]:
                continue
            conversation_ids.append(conversation_id["id"])
        return conversation_ids
    
    def add_message(self, conversation_id, message, role):
        self.chat_history_table.insert_one(
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": message,
                "created_at": int(time.time())
            }
        )

    def get_messages_from_conversation_id(self, 
                                          conversation_id, 
                                          sort_latest=True, 
                                          format_type="dict"):
        cursor = self.chat_history_table.find({'conversation_id' : conversation_id})
        if sort_latest:
            cursor.sort("created_at", DESCENDING)
        
        messages = []
        for message in cursor:
            messages.append(self._format_message(message, format_type))
        return messages
    
    def _format_message(self, message, format_type="dict"):
        if format_type == "dict":
            return {
                "role": message["role"],
                "content": message["content"]
            }
        elif format_type == "str":
            return message["role"] + ": " + message["content"]
        elif format_type == "tuple":
            return (message["role"], message["content"])

    
    