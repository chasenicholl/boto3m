import logging
from boto3m.s3 import S3

logging.getLogger('boto3m').setLevel(logging.DEBUG)

s3 = S3()
files = s3.download('20170802/285c8c9f00d8b387/',
                    # '/tmp/',
                    bucket='carmera-raw-videos')
print(files)

# with downloader.download('test', '/tmp/') as files:
#    print(files)
