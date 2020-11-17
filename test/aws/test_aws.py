from logi_web.utils.aws import aws_cli


data = open('/home/sa/Desktop/large.png', 'rb')

aws_cli.upload_to_s3(name='large.png', data=data)

print("Done")
