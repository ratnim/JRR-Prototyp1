### Installation for REST API Server

- `virtualenv venv`
- (LINUX) `source venv/bin/activate`
- (WINDOWS) `path/to/venv/scripts/activate`
- `pip install -r requirements.txt`
- `python manage.py makemigrations && python manage.py migrate`
- `python manage.py createsuperuser`


### Run REST API Server

- `python manage.py runserver`

### Local Configurations

Create local settings file with
- `python manage.py createlocalsettings`

This settings file is based on `boilerplate.settings.dev`.
Adjust to your needs.
