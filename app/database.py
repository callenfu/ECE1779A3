import boto3
from werkzeug.security import generate_password_hash
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
db = boto3.resource('dynamodb')


#user table class
class DynamoDB:
    usertable = db.Table('UserTable')
    imagetable = db.Table('imagetable')

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

    def check_image(self, item, value):
        response = self.imagetable.get_item(
            Key={
                item: value
            }
        )
        result = None
        if 'Item' in response:
            result = response['Item']
        return result

    def check_email(self,email):
        response = self.usertable.query(
            IndexName="email-index",
            KeyConditionExpression=Key('email').eq(email),)
        result = response['Items'][0]
        return result

    def get_history(self,username):
        response = self.imagetable.query(
            IndexName="username-index",
            KeyConditionExpression=Key('username').eq(username),)
        result = response['Items']
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


    def add_image(self, username, filename):
        image = {
            'username': username,
            'imagename': filename
        }
        response = self.imagetable.put_item(
            Item=image
        )
        return response


