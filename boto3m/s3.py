import boto3
import boto3m.utils as util
import errno
import logging
import math
import multiprocessing
import os
import tempfile
import sys
from concurrent.futures import ProcessPoolExecutor
from config import *


class S3Client(object):

    api = boto3
    client = None

    def __new__(cls):
        return cls._get_client(cls)

    def _get_client(self):
        """
        Gets an instance of boto3 s3 client. Check default env variables
        for credentials.
        """
        if self.client is None:
            args = {}
            if AWS_ACCESS_KEY_ID is not None:
                args['aws_access_key_id'] = AWS_ACCESS_KEY_ID
            if AWS_SECRET_ACCESS_KEY is not None:
                args['aws_secret_access_key'] = AWS_SECRET_ACCESS_KEY
            if AWS_S3_ENDPOINT_URL is not None:
                args['endpoint_url'] = AWS_S3_ENDPOINT_URL
            self.client = self.api.client(
                's3',
                **args
            )
        return self.client


class S3M(object):

    def download(self, keys=None, dest=None, bucket=None):
        """
        Download S3 <keys> in mutliple process to <dest> folder

        :param list|str keys: A list of key path(s). Or a key path.
        :param str dest: The directory to save files to [optional].
        :param str bucket: Source bucket [optional].
        """
        if isinstance(keys, list) is True:
            if len(keys) == 0:
                raise Exception('Input list of download keys is empty.')
        if isinstance(keys, str) is True:
            keys = [keys]

        if dest is None:
            dest = '{}/'.format(tempfile.TemporaryDirectory().name)
            logger.debug('Creating temporary directory: {}'.format(dest))

        if bucket is None:
            bucket = BOTO3M_BUCKET

        to_download = []
        for key in keys:
            if key[-1] == '/':
                logger.debug('Listing keys for s3://{}/{}'.format(bucket,
                                                                  key))
                _keys = self.list_object_keys(Bucket=bucket,
                                              Prefix=key,
                                              MaxKeys=1000)
                to_download.extend(_keys)
            else:
                to_download.append(key)

        # Seperate downloads into chunks to distribute across workers
        chunks = util.chunk(to_download,
                            math.ceil(len(to_download) / BOTO3M_WORKERS))

        # Distrubute across workers
        logger.debug('Distributing downloads '
                     'across {} worker(s).'.format(len(chunks)))
        futures = []
        with ProcessPoolExecutor(max_workers=len(chunks)) as executor:
            for chunk in chunks:
                resp = executor.submit(S3.download_fileobjects,
                                       bucket=bucket,
                                       keys=chunk,
                                       dest=dest)
                futures.append(resp)

        # Collect results and return a list of file locations
        downloaded_files = []
        for future in futures:
            res = future.result()
            if isinstance(res, list):
                downloaded_files.extend(res)
        return downloaded_files

    def list_object_keys(self, **args):
        """
        Recursivly finds object keys
        """
        contents = []
        client = S3Client()

        def _list_objects(args):
            resp = client.list_objects_v2(**args)
            if 'Contents' not in resp:
                return contents
            contents.extend([row['Key'] for row in resp['Contents']])
            if resp['IsTruncated'] is True:
                args['ContinuationToken'] = resp['NextContinuationToken']
                return _list_objects(args)
            else:
                return contents
        return _list_objects(args)

    @staticmethod
    def download_fileobjects(client=None, bucket=None, keys=None, dest=None):
        """
        Create a new Boto3 Session, and download chunk of files.
        Auto create folders along the way.
        """
        client = S3Client()
        files = []
        for key in keys:
            filename = '{}{}'.format(dest, key)
            logger.debug('Downloading: s3://{}/{}'.format(bucket, key))
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filename, 'wb') as data:
                client.download_fileobj(bucket, key, data)
            logger.debug('Downloaded to {}'.format(filename))
            files.append(filename)
        return files
