# backend/payments/utils.py - Enhanced version with better error handling and logging

import stripe
import requests
import base64
from datetime import datetime
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger('payments')
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(project, user):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': project.title,
                    },
                    'unit_amount': int(project.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://website-git-main-kenistances-projects.vercel.app/payment-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://website-git-main-kenistances-projects.vercel.app/payment-cancel',
            metadata={'project_id': project.id, 'user_id': user.id}
        )
        return session.url
    except Exception as e:
        logger.error(f"Stripe session error: {e}")
        return None


def get_mpesa_access_token():
    """
    Generate M-Pesa access token using consumer key and secret
    """
    try:
        logger.info("Requesting M-Pesa access token")
        
        # Check if settings are properly configured
        if not hasattr(settings, 'MPESA_CONSUMER_KEY') or not settings.MPESA_CONSUMER_KEY:
            logger.error("MPESA_CONSUMER_KEY not configured")
            return None
            
        if not hasattr(settings, 'MPESA_CONSUMER_SECRET') or not settings.MPESA_CONSUMER_SECRET:
            logger.error("MPESA_CONSUMER_SECRET not configured")
            return None
            
        if not hasattr(settings, 'MPESA_ACCESS_TOKEN_URL') or not settings.MPESA_ACCESS_TOKEN_URL:
            logger.error("MPESA_ACCESS_TOKEN_URL not configured")
            return None
        
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        
        # Create the basic auth string
        auth_string = f"{consumer_key}:{consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json'
        }
        
        logger.info(f"Making request to: {settings.MPESA_ACCESS_TOKEN_URL}")
        response = requests.get(settings.MPESA_ACCESS_TOKEN_URL, headers=headers, timeout=30)
        logger.info(f"M-Pesa token request status: {response.status_code}")
        logger.info(f"M-Pesa token response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            access_token = result.get('access_token')
            if access_token:
                logger.info("M-Pesa access token generated successfully")
                return access_token
            else:
                logger.error(f"No access_token in response: {result}")
                return None
        else:
            logger.error(f"Failed to get M-Pesa access token: Status {response.status_code}, Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error("M-Pesa access token request timed out")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to M-Pesa token endpoint")
        return None
    except Exception as e:
        logger.error(f"Error generating M-Pesa access token: {e}")
        return None


def generate_mpesa_password():
    """
    Generate M-Pesa password using shortcode, passkey and timestamp
    """
    try:
        if not hasattr(settings, 'MPESA_SHORTCODE') or not settings.MPESA_SHORTCODE:
            logger.error("MPESA_SHORTCODE not configured")
            return None, None
            
        if not hasattr(settings, 'MPESA_PASSKEY') or not settings.MPESA_PASSKEY:
            logger.error("MPESA_PASSKEY not configured")
            return None, None
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        shortcode = str(settings.MPESA_SHORTCODE)
        passkey = settings.MPESA_PASSKEY
        
        # Create the password string
        password_string = f"{shortcode}{passkey}{timestamp}"
        password_bytes = password_string.encode('ascii')
        password_b64 = base64.b64encode(password_bytes).decode('ascii')
        
        logger.info(f"Generated M-Pesa password for timestamp: {timestamp}")
        return password_b64, timestamp
        
    except Exception as e:
        logger.error(f"Error generating M-Pesa password: {e}")
        return None, None


def create_mpesa_payment_request(phone_number, amount, project_id, user_id):
    """
    Create M-Pesa STK Push payment request
    """
    try:
        logger.info(f"Starting M-Pesa payment request for phone: {phone_number}, amount: {amount}")
        
        # Get access token
        access_token = get_mpesa_access_token()
        if not access_token:
            logger.error("Failed to get M-Pesa access token")
            return {
                "success": False,
                "error": "Failed to get M-Pesa access token",
                "errorMessage": "M-Pesa service is temporarily unavailable. Please try again later."
            }
        
        # Generate password and timestamp
        password, timestamp = generate_mpesa_password()
        if not password or not timestamp:
            logger.error("Failed to generate M-Pesa password")
            return {
                "success": False,
                "error": "Failed to generate M-Pesa password",
                "errorMessage": "M-Pesa configuration error. Please contact support."
            }
        
        # Check required settings
        required_settings = ['MPESA_STK_PUSH_URL', 'MPESA_SHORTCODE', 'MPESA_CALLBACK_URL']
        for setting in required_settings:
            if not hasattr(settings, setting) or not getattr(settings, setting):
                logger.error(f"{setting} not configured")
                return {
                    "success": False,
                    "error": f"{setting} not configured",
                    "errorMessage": "M-Pesa configuration error. Please contact support."
                }
        
        # Create unique transaction reference
        transaction_ref = f"PROJECT_{project_id}_{user_id}_{timestamp}"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Convert amount to KES (assuming your project price is in USD)
        # You might want to use a currency conversion API here
        amount_kes = max(1, int(float(amount) * 130))  # Rough USD to KES conversion, minimum 1 KES
        
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount_kes,
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": f"PROJECT_{project_id}",
            "TransactionDesc": f"Payment for project {project_id}"
        }
        
        logger.info(f"Sending M-Pesa STK Push request to: {settings.MPESA_STK_PUSH_URL}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            settings.MPESA_STK_PUSH_URL, 
            json=payload, 
            headers=headers, 
            timeout=30
        )
        
        logger.info(f"M-Pesa STK Push response status: {response.status_code}")
        logger.info(f"M-Pesa STK Push response headers: {dict(response.headers)}")
        logger.info(f"M-Pesa STK Push response: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                response_code = result.get('ResponseCode')
                
                logger.info(f"M-Pesa response parsed: {result}")
                
                if response_code == '0':
                    return {
                        "success": True,
                        "checkoutRequestID": result.get('CheckoutRequestID'),
                        "merchantRequestID": result.get('MerchantRequestID'),
                        "response_code": response_code,
                        "transaction_id": result.get('CheckoutRequestID'),
                        "message": "Payment request sent successfully. Please check your phone.",
                        "amount_kes": amount_kes
                    }
                else:
                    error_desc = result.get('ResponseDescription', f'Payment request failed with code {response_code}')
                    return {
                        "success": False,
                        "error": error_desc,
                        "errorMessage": error_desc,
                        "response_code": response_code
                    }
            except ValueError as json_error:
                logger.error(f"Failed to parse M-Pesa JSON response: {json_error}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response from M-Pesa: {response.text}",
                    "errorMessage": "M-Pesa service returned invalid response. Please try again."
                }
        else:
            logger.error(f"M-Pesa API returned status {response.status_code}")
            
            error_msg = f"M-Pesa API error (Status {response.status_code})"
            try:
                error_data = response.json()
                error_msg = error_data.get('errorMessage', error_data.get('ResponseDescription', error_msg))
                logger.error(f"M-Pesa error details: {error_data}")
            except:
                error_msg = response.text or error_msg
                logger.error(f"M-Pesa raw error response: {response.text}")
            
            return {
                "success": False,
                "error": f"M-Pesa API error: {error_msg}",
                "errorMessage": "Payment request failed. Please try again.",
                "status_code": response.status_code
            }
            
    except requests.exceptions.Timeout:
        logger.error("M-Pesa STK Push request timed out")
        return {
            "success": False,
            "error": "Request timed out",
            "errorMessage": "Payment request timed out. Please try again."
        }
    
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to M-Pesa API")
        return {
            "success": False,
            "error": "Connection error",
            "errorMessage": "Unable to connect to payment service. Please check your internet connection and try again."
        }
    
    except Exception as e:
        logger.error(f"M-Pesa STK Push error: {e}")
        logger.exception("Full M-Pesa error traceback:")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "errorMessage": "Payment request failed. Please try again."
        }


def verify_mpesa_payment(checkout_request_id):
    """
    Verify M-Pesa payment status using checkout request ID
    """
    try:
        logger.info(f"Verifying M-Pesa payment: {checkout_request_id}")
        
        access_token = get_mpesa_access_token()
        if not access_token:
            return {"success": False, "error": "Failed to get access token"}
        
        password, timestamp = generate_mpesa_password()
        if not password or not timestamp:
            return {"success": False, "error": "Failed to generate password"}
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        query_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpushquery/v1/query"
        logger.info(f"Querying M-Pesa status at: {query_url}")
        
        response = requests.post(query_url, json=payload, headers=headers, timeout=30)
        
        logger.info(f"M-Pesa query response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "result_code": result.get('ResultCode'),
                "result_desc": result.get('ResultDesc'),
                "data": result
            }
        else:
            return {
                "success": False,
                "error": "Failed to verify payment",
                "status_code": response.status_code,
                "response": response.text
            }
            
    except Exception as e:
        logger.error(f"M-Pesa payment verification error: {e}")
        return {
            "success": False,
            "error": str(e)
        }