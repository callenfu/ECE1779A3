import boto3
from werkzeug.security import generate_password_hash

# Get the service resource.
db = boto3.resource('dynamodb')


#user table class
class UserTable:
    usertable = db.Table('UserTable')

    def add_user(self, username, password, email ):
        password_hash = generate_password_hash(password)
        user = {
            'username': username,
            'password_hash': password_hash,
            'admin_auth': False,
            'email': email
        }
        self.usertable.put_item(
            Item=user
        )

    def check_item(self,item,value):
        response = self.usertable.get_item(
            Key={
                item: value
            }
        )
        result = None
        if 'Item' in response:
            result = response['Item']
        return result


    def update_password_username(self,username, password_hash):
        response = self.usertable.update_item(
            Key={
                'username': username
            },
            UpdateExpression="set password_hash=:r",
            ExpressionAttributeValues={
                ':r': password_hash
            },
            ReturnValues="UPDATED_NEW"
        )
        return response


