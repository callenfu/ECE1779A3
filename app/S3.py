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


def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=3600)
    # The response contains the presigned URL
    return response