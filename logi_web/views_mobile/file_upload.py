from io import BytesIO

from aiohttp import web, BodyPartReader

from logi_web.utils.aws import aws_cli


class FileUpload:
    def __init__(self) -> None:
        super().__init__()


    @staticmethod
    async def delete_signature():
        pass


    @staticmethod
    async def file_upload_test(request: web.Request):
        file = None
        obj: BodyPartReader
        filename: str
        async for obj in (await request.multipart()):
            # obj is an instance of aiohttp.multipart.BodyPartReader
            if obj.filename is not None:  # to pass non-files
                file = BytesIO(await obj.read())
                filename = obj.filename

        await aws_cli.upload_to_s3(filename, file)

        return web.Response(
            text=f'{filename} successfully stored')


file_upload_mobile = FileUpload()
