import boto3

s3 = boto3.client('s3')
bucket_name = 'ece1779a3project'

def get_image(filename):
    file = boto3.resource('s3')
    obj = file.Object(bucket_name,filename)
    body = obj.get()['Body'].read()
    return body



def clear_s3():
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        print(key['Key'])
        s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': [
                    {
                        'Key': key['Key'],
                        # 'VersionId': 'string'
                    },
                ],
                'Quiet': True
            },
        )


def upload_file(file, filename):
    #s3.upload_file(dirname, bucket_name, filename)
    s3.upload_fileobj(file, bucket_name,filename)