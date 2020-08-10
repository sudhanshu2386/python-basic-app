from app import app
from config import client
from flask import request, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import ast


# Select the database 
db = client.OSS_DEV_API
# Select the collection
collection = db.Users


# Function to get General response
@app.route("/")
def get_initial_response() :
    """Welcome message for the API"""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    #Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp

# Function to Create users
@app.route("/api/v1/users", methods=['POST'])
def create_users() :
    try :
        # Create new users
        try :
            body = ast.literal_eval(json.dumps(request.get_json()))
        except :
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "Request Body invalid !!", 400
           
        record_created = collection.insert(body)

        # Prepare the response
        if isinstance(record_created, list) :
            # Return list of Id of the newly created user
            return jsonify([str(v) for v in record_created]), 201
        else :
            # Return id of newly created user
            return jsonify(str(record_created)), 201
     
    except :
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "error while creating User !!", 500


# Function to Fetch users  
@app.route("/api/v1/users", methods=['GET'])
def fetch_users() :
    try :
        # Fetch all the record(s)
        records_fetched = collection.find()

        users_arr = []
        # Check if the records are found
        if records_fetched.count() > 0 :
            # Prepare the response
            for document in records_fetched :
                document['_id'] = str(document['_id'])
                users_arr.append(document)
            return jsonify(users_arr), 201
        else :
            # No records are found
            return "User not found  !!", 404
        
    except :
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "Error while trying to fetch the users !!", 500


# Function to Fetch users by Id
@app.route("/api/v1/users/<_id>", methods=['GET'])
def fetch_users_by_id(_id) :
    try :
        # Fetch user by Id
        record_fetched = collection.find_one({"_id": ObjectId(_id)})

         # Check if resource is fetched
        if record_fetched is not None :
            # Prepare the response as resource is fetched successfully
            return dumps(record_fetched), 201
        else :
             # Bad request as the resource is not available
             # Add message for debugging purpose
             return "User is not available !!", 404
    except :
         # Error while trying to update the resource
        # Add message for debugging purpose
        return "Error while trying to fetch the User !!", 500
    


# Function to Update user
@app.route("/api/v1/users/<_id>", methods=['PATCH'])
def update_user(_id) :
    try :
        # Get the value which needs to be updated
        try :
            body = ast.literal_eval(json.dumps(request.get_json()))
        except :
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "Request Body invalid !!", 400

        # Updating the user
        record_updated = collection.update_one({"_id": ObjectId(_id)}, body)

        # Check if resource is updated
        if record_updated.modified_count > 0 :
            # Prepare the response as resource is updated successfully
            return "User updated successfully !!", 200
        else :
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "User is not available to update !!", 404

    except :
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "Error while trying to update the User !!", 500


#  Function to Delete user by Id

@app.route("/api/v1/users/<_id>", methods=['DELETE'])
def delete_user(_id) :
    try :
        # Delete the user
        delete_user = collection.delete_one({"_id": ObjectId(_id)})

        if delete_user.deleted_count > 0 :
            # Prepare the response
            return "User deleted successfully !!", 200
        else :
            return "User not found !!", 404

    except :
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "Error while trying to delete the User !!", 500

