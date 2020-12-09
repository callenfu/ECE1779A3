import boto3

s3 = boto3.resource('s3')
response = s3.Object('ece1779a3project',)


s3.delete_object(Bucket=bucket, Key=key)