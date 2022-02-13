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

**Note**: This project is built using PostgreSQL Database
**Note**: All DB congfigurations are in .env file
**Note**: All Mailing server congfigurations are in .env file
**Note**: You have to set ENVIRONMENT='production' when going live.
