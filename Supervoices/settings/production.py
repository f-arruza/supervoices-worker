from .base import *

DEBUG = False

# AWS Config
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Broker Config
BROKER_URL = 'sqs://' + AWS_ACCESS_KEY_ID + ':'
BROKER_URL = BROKER_URL + AWS_SECRET_ACCESS_KEY + '@'

# Email Account Config
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_PORT = 587
EMAIL_FROM_MAIL = 'freeven2016@gmail.com'

# S3 Config
AWS_PRELOAD_METADATA = True
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_STORAGE_BUCKET_NODE_NAME = 'supervoices-node'
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
AWS_S3_NODE_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NODE_NAME
AWS_S3_HOST = os.environ['AWS_S3_HOST']

# DynamoDB Config
AWS_DYNAMODB_ENDPOINT = 'https://dynamodb.us-east-1.amazonaws.com'
AWS_DYNAMODB_REGION = 'us-east-1'

# Static files (javascript, css, images)
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'Supervoices.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

# Media files (Images, Audios, Videos)
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
MEDIA_NODE_URL = "https://%s/" % (AWS_S3_NODE_CUSTOM_DOMAIN)
DEFAULT_FILE_STORAGE = 'Supervoices.custom_storages.MediaStorage'
MEDIA_TMP = BASE_DIR + '/tmp/'

# Memcached Config
"""CACHES = {
    'default': {
        'BACKEND': 'django_elasticache.memcached.ElastiCache',
        'LOCATION': 'svs-cache.qzzrzn.cfg.use1.cache.amazonaws.com:11211',
        'OPTIONS': {
            'IGNORE_CLUSTER_ERRORS': [True, False],
        },
    }
}"""
