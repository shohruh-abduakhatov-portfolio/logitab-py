import aioboto3


ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'logitab-signature'

async def upload(
    suite: str,
    release: str,
    filename: str,
    staging_path: Path,
    bucket: str,
) -> str:
    blob_s3_key = f"{suite}/{release}/{filename}"

    async with aioboto3.client("s3") as s3:
        try:
            with staging_path.open("rb") as spfp:
                LOG.info(f"Uploading {blob_s3_key} to s3")
                await s3.upload_fileobj(spfp, bucket, blob_s3_key)
                LOG.info(f"Finished Uploading {blob_s3_key} to s3")
        except Exception as e:
            LOG.error(f"Unable to s3 upload {staging_path} to {blob_s3_key}: {e} ({type(e)})")
            return ""

    return f"s3://{blob_s3_key}"
