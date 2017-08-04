# Boto 3 - M(ultiprocessing) extension.

Boto3m(ultiprocessing) is a simple extension to the Boto3 AWS SDK to support
multiprocess downloading and uploading.

With support for downloading and uploading objects by folders and keys.

### Requirements

Obviously `boto3` is required. Python >= 3.5 is recommended. Come on people. Lets move on from 2.7.

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

Additionally the `S3M` class has 2 environment variables.

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
