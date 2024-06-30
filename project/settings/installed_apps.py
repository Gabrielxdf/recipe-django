# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django Rest Framework
    'rest_framework',
    'rest_framework_simplejwt',
    # CORS Headers
    'corsheaders',
    # Our apps
    'recipes',
    'authors',
    'tag',
]
