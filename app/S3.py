import boto3

s3 = boto3.client('s3')
bucket_name = 'zappa-bucket-a3'



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


def upload_file(dirname, filename):
    s3.upload_file(dirname + '/' + filename, bucket_name, filename)