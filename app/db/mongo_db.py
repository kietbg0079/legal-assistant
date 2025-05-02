from pymongo import MongoClient
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

    def create_conversation(self):
        """Create a new conversation ID"""
        return str(uuid.uuid4())
    
    def add_user(self, user_id, user_info: UserInfoSchema):
        if self.user_table.find_one({'id' : user_id}):
            logger.warning(f"Add info user {user_id} failed: user_id existed")
            return
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
        return UserInfoSchema(**user_info)
    
    def log_message(self, conversation_id, message, role, metadata=None):
        """
        Log a single message in a conversation.
        
        Args:
            conversation_id (str): Unique ID for the conversation
            message (str): Content of the message
            role (str): 'user' or 'assistant'
            metadata (dict, optional): Additional metadata to store
            
        Returns:
            str: ID of the inserted document
        """
        if metadata is None:
            metadata = {}
            
        message_doc = {
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow(),
            "role": role,
            "content": message,
            "metadata": metadata
        }
        
        result = self.collection.insert_one(message_doc)
        return str(result.inserted_id)
    
    def log_interaction(self, conversation_id, user_message, assistant_response, metadata=None):
        """
        Log a complete user-assistant interaction.
        
        Args:
            conversation_id (str): Unique ID for the conversation
            user_message (str): User's message
            assistant_response (str): Assistant's response
            metadata (dict, optional): Additional metadata to store
            
        Returns:
            tuple: IDs of the inserted documents (user_msg_id, assistant_msg_id)
        """
        user_msg_id = self.log_message(conversation_id, user_message, 'user', metadata)
        assistant_msg_id = self.log_message(conversation_id, assistant_response, 'assistant', metadata)
        
        return user_msg_id, assistant_msg_id
    
    def get_conversation_history(self, conversation_id, limit=None):
        """
        Retrieve the history of a conversation.
        
        Args:
            conversation_id (str): Unique ID for the conversation
            limit (int, optional): Maximum number of messages to retrieve
            
        Returns:
            list: List of message documents
        """
        query = {"conversation_id": conversation_id}
        cursor = self.collection.find(query).sort("timestamp", 1)
        
        if limit:
            cursor = cursor.limit(limit)
            
        return list(cursor)
    
    def get_user_conversations(self, user_id, limit=None):
        """
        Retrieve all conversations for a specific user.
        
        Args:
            user_id (str): Unique ID for the user
            limit (int, optional): Maximum number of conversations to retrieve
            
        Returns:
            dict: Dictionary of conversation_id to list of messages
        """
        query = {"metadata.user_id": user_id}
        distinct_conversations = self.collection.distinct("conversation_id", query)
        
        if limit:
            distinct_conversations = distinct_conversations[:limit]
            
        result = {}
        for conv_id in distinct_conversations:
            result[conv_id] = self.get_conversation_history(conv_id)
            
        return result
    
    def search_conversations(self, query_text, metadata_filters=None):
        """
        Search conversations by content or metadata.
        
        Args:
            query_text (str): Text to search for in message content
            metadata_filters (dict, optional): Filters for metadata fields
            
        Returns:
            list: List of matching message documents
        """
        search_query = {"content": {"$regex": query_text, "$options": "i"}}
        
        if metadata_filters:
            for key, value in metadata_filters.items():
                search_query[f"metadata.{key}"] = value
                
        return list(self.collection.find(search_query))
    
    def delete_conversation(self, conversation_id):
        """
        Delete an entire conversation.
        
        Args:
            conversation_id (str): Unique ID for the conversation
            
        Returns:
            int: Number of deleted documents
        """
        result = self.collection.delete_many({"conversation_id": conversation_id})
        return result.deleted_count
    
    def close(self):
        """Close the MongoDB connection"""
        self.client.close()