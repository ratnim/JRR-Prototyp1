### Installation for REST API Server

- `virtualenv venv`
- (LINUX) `source venv/bin/activate`
- (WINDOWS) `path/to/venv/bin/scripts/activate`
- `pip install -r requirements.txt`
- `python manage.py makemigrations && python manage.py migrate`
- `python manage.py createsuperuser`

### Run REST API Server

- `python manage.py runserver`
