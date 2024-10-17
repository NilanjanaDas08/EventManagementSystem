# Installing venv
echo "Initializing New Python Virtual Environment"
python3 -m venv venv

# Activating venv
echo "Activating Virtual Environment"
source venv/bin/activate

# Installing Django
echo "Installing Django"
venv/bin/python -m pip install Django

# Installing Pillow for ImageField
echo "Installing Pillow"
venv/bin/python -m pip install Pillow

# Installing Faker and Django Seed for Seeder
echo "Installing Faker and Django-seed"
venv/bin/python -m pip install faker django-seed

# Installing Requests
echo "Installing Requests"
venv/bin/python -m pip install requests

# Installing Django-Paypal
echo "Installing django-paypal"
venv/bin/python -m pip install django-paypal

# Installing Dotenv
echo "Installing dotenv"
venv/bin/python -m pip install python-dotenv

# Installing Weasyprint
echo "Installing weasyprint"
venv/bin/python -m pip install weasyprint

# Installing QRCode
echo "Installing qrcode"
venv/bin/python -m pip install qrcode

# Just in case, deactivating Virtual Environment
echo "Deactivating Virtual Environment"
deactivate
