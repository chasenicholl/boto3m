# Suppress some logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('s3transfer').setLevel(logging.WARNING)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(process)d %(name)s %(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger('boto3m')


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', None)

BOTO3M_WORKERS = int(os.getenv('BOTO3M_WORKERS', multiprocessing.cpu_count()))
BOTO3M_BUCKET = os.getenv('BOTO3M_BUCKET', None)
