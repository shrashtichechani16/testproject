# Clone the project


# Create Python 3 virtual environment 
python3 -m venv venv
# Activate the virtual environment
. venv/bin/activate

# Install required packages (Django 2.2 LTS)
pip install -r requirements.txt

cd apps
# Create database tables for the project, project configured to use SQLite DB
./manage.py migrate

# Run the development server
./manage.py runserver

habrie is the name of project
student is the app name
add your email id and password to perform send mail functionality : IN habrie>settings.py  add EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
