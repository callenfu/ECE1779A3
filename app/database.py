import boto3
from werkzeug.security import generate_password_hash

# Get the service resource.
db = boto3.resource('dynamodb')


#user table class
class UserTable:
    usertable = db.Table('UserTable')

    def add_user(self,username, password, usertype):
        password_hash = generate_password_hash(password)
        user = {
            'username': username,
            'password_hash': password_hash,
            'usertype': usertype
        }
        self.usertable.put_item(
            Item=user
        )

    def check_user(self,username):
        response = self.usertable.get_item(
            Key={
                'username': username
            }
        )
        user = None
        if 'Item' in response:
            user = response['Item']
        return user


    def verify_user(self):
        pass

mytable = UserTable()

print(mytable.check_user("callen"))

