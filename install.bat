@echo off
echo Initializing New Python Virtual Environment
python -m venv venv

echo Activating Virtual Environment
call venv\Scripts\activate.bat

echo Installing Django
pip install Django

echo Installing Decouple
pip install python-decouple

echo Installing Pillow
pip install Pillow

echo Installing Faker and Django-seed
pip install faker django-seed

echo Installing Requests
pip install requests

echo Installing django-paypal
pip install django-paypal

echo Installing dotenv
pip install python-dotenv

echo Installing weasyprint
pip install weasyprint

echo Installing xhtml2pdf
pip install xhtml2pdf

echo Installing qrcode
pip install qrcode

echo Deactivating Virtual Environment
deactivate