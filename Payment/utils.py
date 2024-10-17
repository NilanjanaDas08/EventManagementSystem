from django.conf import settings
import requests

def verify_pdt(pdt_token):
    """Verify the PDT token with PayPal."""
    payload = {
        'cmd': '_notify-synch',
        'tx': pdt_token,
        'at': settings.PAYPAL_PDT_TOKEN  # This is the PDT token from your PayPal account
    }
    response = requests.post('https://www.sandbox.paypal.com/cgi-bin/webscr', data=payload) #Should remove sandbox for live testing

    # Log the full response text and status code for further inspection
    response_text = response.text

    # Parse the response, PayPal returns "SUCCESS" or "FAIL" followed by the transaction details
    response_data = response_text.split('\n')

    if response_data[0] == 'SUCCESS':
        pdt_info = dict(line.split('=') for line in response_data[1:] if '=' in line)
        return pdt_info
    
    return None