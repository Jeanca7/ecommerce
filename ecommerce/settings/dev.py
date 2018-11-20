from .base import *

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )


MEDIA_URL = '/media/'    #for the pictures/images
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
