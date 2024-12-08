import os
import pymongo
from pymongo.errors import OperationFailure
from pymongo.mongo_client import MongoClient
from pymongo import errors
import hashlib
import json

def get_collection(bot_name, mongo_uri):
    client = MongoClient(mongo_uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except errors.OperationFailure as e:
        raise ValueError(f"Failed to connect to MongoDB: {e}")

    # Generate a unique collection name using the bot token
    collection_name = hashlib.md5(bot_name.encode()).hexdigest()
    db = client['Luminant']
    return db[collection_name]

def save_name(collection, name):
    # Save name to local file
    with open("name.txt", "w") as file:
        file.write(name)
    
    # Check if name already exists in MongoDB
    existing_name = collection.find_one()
    if existing_name:
        # Update existing name in MongoDB
        collection.update_one({}, {"$set": {"name": name}})
    else:
        # Insert new name into MongoDB
        collection.insert_one({"name": name})

def load_name(collection):
    try:
        # Try to load name from local file
        with open("name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    # Load name from MongoDB
    result = collection.find_one()
    if result:
        return result.get("name")  # Use get method to avoid KeyError
    else:
        return None

def save_accept_logs(collection, accept_logs):
    # Save accept_logs to local file
    with open("accept_logs.txt", "w") as file:
        file.write(str(accept_logs))
    
    # Check if accept_logs already exists in MongoDB
    existing_logs = collection.find_one({"accept_logs": {"$exists": True}})
    if existing_logs:
        # Update existing accept_logs in MongoDB
        collection.update_one({}, {"$set": {"accept_logs": accept_logs}})
    else:
        # Insert new accept_logs into MongoDB
        collection.insert_one({"accept_logs": accept_logs})

def load_accept_logs(collection):
    try:
        # Try to load accept_logs from local file
        with open("accept_logs.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    # Load accept_logs from MongoDB
    result = collection.find_one({"accept_logs": {"$exists": True}})
    if result:
        return result.get("accept_logs")  # Use get method to avoid KeyError
    else:
        return 0

def save_authorized_users(collection, authorized_users):
    # Save authorized users to local file
    with open("authorized_users.txt", "w") as file:
        for user_id in authorized_users:
            file.write(str(user_id) + "\n")
    
    # Check if authorized users already exist in MongoDB
    existing_users = collection.find_one({"type": "authorized_users"})
    if existing_users:
        # Update existing authorized users in MongoDB
        collection.update_one({"type": "authorized_users"}, {"$set": {"value": authorized_users}})
    else:
        # Insert new authorized users into MongoDB
        collection.insert_one({"type": "authorized_users", "value": authorized_users})

def load_authorized_users(collection):
    try:
        # Try to load authorized users from local file
        with open("authorized_users.txt", "r") as file:
            return [int(user_id) for user_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    # Load authorized users from MongoDB
    result = collection.find_one({"type": "authorized_users"})
    if result:
        return result.get("value", [])  # Use get method to avoid KeyError
    else:
        return []  # Default value if not found in MongoDB

def save_allowed_channel_ids(collection, allowed_channel_ids):
    # Save allowed channel IDs to local file
    with open("allowed_channel_ids.txt", "w") as file:
        for channel_id in allowed_channel_ids:
            file.write(str(channel_id) + "\n")
    
    # Check if allowed channel IDs already exist in MongoDB
    existing_channels = collection.find_one({"type": "allowed_channel_ids"})
    if existing_channels:
        # Update existing allowed channel IDs in MongoDB
        collection.update_one({"type": "allowed_channel_ids"}, {"$set": {"value": allowed_channel_ids}})
    else:
        # Insert new allowed channel IDs into MongoDB
        collection.insert_one({"type": "allowed_channel_ids", "value": allowed_channel_ids})

def load_allowed_channel_ids(collection):
    try:
        # Try to load allowed channel IDs from local file
        with open("allowed_channel_ids.txt", "r") as file:
            return [int(channel_id) for channel_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    # Load allowed channel IDs from MongoDB
    result = collection.find_one({"type": "allowed_channel_ids"})
    if result:
        return result.get("value", [])  # Use get method to avoid KeyError
    else:
        return []  # Default value if not found in MongoDB

def save_log_channel_id(collection, log_channel_id):
    # Save log channel ID to local file
    with open("log_channel_id.txt", "w") as file:
        file.write(str(log_channel_id))
    
    # Check if log channel ID already exists in MongoDB
    existing_log_channel = collection.find_one({"type": "log_channel_id"})
    if existing_log_channel:
        # Update existing log channel ID in MongoDB
        collection.update_one({"type": "log_channel_id"}, {"$set": {"value": log_channel_id}})
    else:
        # Insert new log channel ID into MongoDB
        collection.insert_one({"type": "log_channel_id", "value": log_channel_id})

def load_log_channel_id(collection):
    try:
        # Try to load log channel ID from local file
        with open("log_channel_id.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    # Load log channel ID from MongoDB
    result = collection.find_one({"type": "log_channel_id"})
    if result:
        return result.get("value", -1)  # Use get method to avoid KeyError
    else:
        return -1  # Default value if not found in MongoDB


#===================== SAVING AND LOADING BOT RUNNING TIME ===========================

def save_bot_running_time(collection, time_to_add):
    current_time = collection.find_one({"type": "bot_running_time"})
    if current_time:
        total_time = current_time['time'] + time_to_add
        collection.update_one({"type": "bot_running_time"}, {"$set": {"time": total_time}})
    else:
        total_time = time_to_add
        collection.insert_one({"type": "bot_running_time", "time": total_time})
    return total_time


def load_bot_running_time(collection):
    current_time = collection.find_one({"type": "bot_running_time"})
    return current_time['time'] if current_time else 0


def reset_bot_running_time(collection, new_time=0):
    collection.update_one({"type": "bot_running_time"}, {"$set": {"time": new_time}}, upsert=True)


def save_max_running_time(collection, max_time):
    collection.update_one({"type": "max_running_time"}, {"$set": {"time": max_time}}, upsert=True)


def load_max_running_time(collection):
    current_time = collection.find_one({"type": "max_running_time"})
    return current_time['time'] if current_time else 800 * 3600  # Default to 800 hours in seconds

#============ QUEUE FILE SAVING AND LOADING ================

# Function to save the file queue to MongoDB
def save_queue_file(collection, file_queue):
    collection.delete_many({})  # Clear existing queue
    if file_queue:
        collection.insert_one({"type": "file_queue", "file_queue_data": file_queue})  # Save queue to MongoDB

# Function to load the file queue from MongoDB
def load_queue_file(collection):
    result = collection.find_one({"type": "file_queue"})
    return result['file_queue_data'] if result else []

