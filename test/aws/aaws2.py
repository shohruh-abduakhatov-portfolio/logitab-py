import asyncio

import aiobotocore


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''


async def go():
    bucket = 'logitab-signature'
    filename = 'large2.png'

    data = open('/home/sa/Desktop/large.png', 'rb')

    folder = 'public-signatur'
    key = f'{folder}/{filename}'
    file_url = f'https://logitab-signature.s3.us-east-2.amazonaws.com/public-signatur/{filename}'

    session = aiobotocore.get_session()
    async with session.create_client(
            's3', region_name='us-west-2',
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            # config=Config(signature_version='s3v4')
    ) as client:
        # upload object to amazon s3
        resp = await client.put_object(Bucket=bucket,
                                       Key=key,
                                       Body=data)
        print(resp)

        # getting s3 object properties of file we just uploaded
        # resp = await client.get_object_acl(Bucket=bucket, Key=key)
        # print(resp)

        # delete object from s3
        # resp = await client.delete_object(Bucket=bucket, Key=key)
        # print(resp)


loop = asyncio.get_event_loop()
loop.run_until_complete(go())
