# Media Directory

All media files saved in /media in the base directory, so you have to serve and protect it.

## Installation

# Step 1:
```bash
$ pip install -r requirements.txt
```

# Step 2:
You have to run the following commands on every pull:

### 1: Migrate the new changes to the DB.
```bash
$ python manage.py migrate
```
### 2: Collect Static files
```bash
$ python manage.py collectstatic
```

# To create a super user you have to run the following command:
```bash
$ python manage.py createsuperuser
```

# --- Configurations

**Note**: This project is built using PostgreSQL Database

**Note**: All DB configurations are in .env file

**Note**: All Mailing server configurations are in .env file

**Note**: You have to set environment='production' when going live.

**Note**: You have to set FRONT_END_DOMAIN='https://front-domain.com' when going live.

**Note**: You have to set ALLOWED_HOST='back-domain.com' without http:// when going live.
