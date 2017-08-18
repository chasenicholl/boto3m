# Boto 3M(ultiprocessing) extension.

Boto3m(ultiprocessing) is a simple extension to the Boto3 AWS SDK to support
multiprocess downloading (and uploading coming soon).

With support for downloading (and uploading coming soon) objects by folders and keys.

### Requirements

Obviously `boto3` is required. Python >= 3.5 is recommended. (Come on people, lets move on from 2.7)

```
$ pip install boto3
```

### Installation

```
$ git clone git@github.com:chasenicholl/boto3m.git
$ cd boto3m && python3 setup.py install --upgrade
```

### Configuring

Configuration follows boto3's pattern. See http://boto3.readthedocs.io/en/latest/guide/configuration.html.

Additionally when using boto3m, 2 optional environment variables my be set.

```python
BOTO3M_WORKERS = 8  # This is the number of parallel processes boto3m can use.
                    # Defaults to systems CPU count.
BOTO3M_BUCKET = 'some_bucket_on_s3'  # The target bucket.
                                     # This can also be passed as a method argument.
```


### Usage Example

```python
import logging
from boto3m.s3 import S3M


# Set log level to DEBUG to see output
logging.getLogger('boto3m').setLevel(logging.DEBUG)


# 1. Download by S3 folder. 
# This will automatically find all keys within remote folder.
# Returns a list of downloaded files local location.
files = S3M().download('some/folder/on/s3/',
                      bucket='my-cool-s3-bucket')


# 2. Download by S3 folder to SPECIFIC location 
# This will automatically find all keys within remote folder to a SPECIFIC local destination.
# Returns a list of downloaded files local location.
files = S3M().download('some/folder/on/s3/',
                      dest='/tmp/',
                      bucket='my-cool-s3-bucket')


# 3. Download by S3 keys
# This will download specific S3 keys.
# Returns a list of downloaded files local location.
files = S3M().download(['file1.jpg', 'file2.jpg', 'file3.jpg'],
                      bucket='my-cool-s3-bucket')

```
