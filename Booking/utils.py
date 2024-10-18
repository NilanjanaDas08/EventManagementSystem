import qrcode
import io
import base64
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from weasyprint import HTML # In case of gobject error, comment out code
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from django.conf import settings
# from cryptography.fernet import Fernet
import os

def generate_qr_code(data):
    # Could look into Encrypting Data using Fernet Cipher to actually implement QR code scan
    # key = Fernet
    # cipher = Fernet(Fernet.generate_key()).encrypt(data)

    # Generating QR Code with given data into base64 string
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Convert qr to image
    img = qr.make_image(fill = 'black', back_color = 'white')

    # Saving image to byte stream
    img_bytes = io.BytesIO()
    img.save(img_bytes)

    # Encoding image to base64 
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return img_base64

def render_pdf_view(request, pdf_config: dict):
    """Creates PDF ticket using given context"""

    html = render_to_string("ticket.html",pdf_config)
    pdf_buffer = io.BytesIO()

    # Using xhtml2pdf for Windows
    if os.name == 'nt':
        pisa_status = pisa.CreatePDF(
            html,
            dest = pdf_buffer,
            link_callback=link_callback
        )

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # Using weasyprint for Linux (In case of gobject error in Windows, comment out else block)
    else:
        static_url = request.build_absolute_uri(settings.STATIC_URL)
        HTML(string=html, base_url=static_url).write_pdf(pdf_buffer)

    pdf_buffer.seek(0)

    return pdf_buffer

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    # Check if the URI is related to static files
    sUrl = settings.STATIC_URL  # Static URL (e.g., "/static/")
    sRoot = settings.STATIC_ROOT  # Path to static files directory (e.g., "/path/to/staticfiles")

    mUrl = settings.MEDIA_URL  # Media URL (e.g., "/media/")
    mRoot = settings.MEDIA_ROOT  # Path to media directory (e.g., "/path/to/media/")

    # If the URI is a static URL, resolve it within STATIC_ROOT
    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ''))
        if os.path.isfile(path):
            return path

    # If the URI is a media URL, resolve it within MEDIA_ROOT
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ''))
        if os.path.isfile(path):
            return path

    # If it's neither static nor media, return the original URI (it may be an external link)
    return uri