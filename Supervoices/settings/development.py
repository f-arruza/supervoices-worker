from .base import *

DEBUG = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_ROOT = BASE_DIR + '/static/'

# Media files (Images, Audios, Videos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media/'

# Broker Config
BROKER_URL = 'amqp://' + os.environ['AMQP_USER'] + ':'
BROKER_URL = BROKER_URL + os.environ['AMQP_PASSWORD'] + '@'
BROKER_URL = BROKER_URL + os.environ['AMQP_HOST'] + ':5672//'

# Email Account Config
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_FROM_MAIL = 'freeven2016@gmail.com'
