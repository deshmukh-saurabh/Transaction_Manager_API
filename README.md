## A Transaction Manager API built using Django REST Framework, PostgreSQL

Users register and create a wallet(one per user). Transactions can then be performed from one wallet to the other.

## Features
- Authorization
- Pagination
- Filters
- Throttling

### 1. Install dependencies
```sh
pip install -r requirements.txt
```

### 2. Create a .env file
- Add your django app Secret key, Database name, user and password to it as shown below
```sh
SECRET_KEY=<your_secret_key_without_quotes>
DB_NAME=<your_db_name_without quotes>
DB_USER=<your_db_user_without_quotes>
DB_PASSWORD=<your_db_password_without_quotes>
```

### 3. Database used is PostgreSQL, make sure you add your own credentials in the .env file
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Replace with your desired name in the .env file
        'NAME': os.environ['DB_NAME'],
        # Replace username with your user name in the .env file
        'USER': os.environ['DB_USER'],
        # Replace password with your password in the .env file
        'PASSWORD': os.environ['DB_PASSWORD'],
        # Replace 127.0.0.1 with the PostgreSQL host
        'HOST': '127.0.0.1',
        # Replace 5432 with the PostgreSQL configured port
        # in case you aren't using the default port
        'PORT': '5432',
    }
}
```

### 4. Serve API on localhost:8000
```sh
python transaction_manager/manage.py runserver
```

### 5. Use postman to test it.

Extensive documentation with examples [here](https://documenter.getpostman.com/view/10646104/TVCiSRRA).
