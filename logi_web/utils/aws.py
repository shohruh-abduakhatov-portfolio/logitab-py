import aiobotocore


class AwsCli:


    def __init__(self) -> None:
        super().__init__()
        self.session = aiobotocore.get_session()


    async def upload_to_s3(self, filename, data):
        key = f'{self.SIGNATURE_FOLDER}/{filename}'
        async with self.session.create_client(
                's3',
                aws_secret_access_key=self.ACCESS_SECRET_KEY,
                aws_access_key_id=self.ACCESS_KEY_ID,
        ) as client:
            try:
                # upload object to amazon s3
                resp = await client.put_object(Bucket=self.BUCKET_NAME,
                                               Key=key,
                                               Body=data)
                print(resp)
            except Exception as ex:
                raise ex
        return f'{self.BASE_URL}/{key}'


    async def delete_s3(self, key):
        async with self.session.create_client(
                's3',
                aws_secret_access_key=self.ACCESS_SECRET_KEY,
                aws_access_key_id=self.ACCESS_KEY_ID,
        ) as client:
            # delete object from s3
            try:
                resp = await client.delete_object(Bucket=self.BUCKET_NAME, Key=key)
                print(resp)
            except Exception as ex:
                raise ex


aws_cli = AwsCli()
