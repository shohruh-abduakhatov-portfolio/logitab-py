from config_loader import child_config
from modules.core.AbstractExecutor import *


class AwsS3Executor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.session = aiobotocore.get_session()


    async def test(self):
        print("ok")


    async def delete_file(self, filename):
        async with self.session.create_client(
                's3', region_name=child_config.aws_region_name,
                aws_secret_access_key=child_config.aws_access_key,
                aws_access_key_id=child_config.aws_key_id,
        ) as client:
            for i in range(4):
                try:
                    # delete object from s3
                    resp = await client.delete_object(
                        Bucket=child_config.aws_bucket,
                        Key=filename)
                    assert resp
                    resp = json.loads(resp)
                    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
                    return filename
                except:
                    await asyncio.sleep(1)


    async def push_file(self, file, filename: str):
        path = f'{child_config.aws_uri}/{filename}'
        async with self.session.create_client(
                's3', region_name=child_config.aws_region_name,
                aws_secret_access_key=child_config.aws_access_key,
                aws_access_key_id=child_config.aws_key_id,
        ) as client:
            for i in range(4):
                try:
                    # upload object to amazon
                    resp = await client.put_object(
                        Bucket=child_config.aws_bucket,
                        Key=filename,
                        Body=file)
                    assert resp
                    resp = json.loads(resp)
                    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
                    return path
                except:
                    await asyncio.sleep(1)


    async def push_report(self, file, filename):
        path = f'log-edit-report/{filename}'
        return await self.push_file(file, path)


    async def push_signature(self, file, filename):
        path = f'driver_signature/{filename}'
        return await self.push_file(file, path)
