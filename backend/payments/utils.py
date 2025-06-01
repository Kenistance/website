import stripe
import requests
from django.conf import settings

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
    except Exception:
        return None


def create_mpesa_payment_request(phone_number, amount, project_id, user_id):
    url = settings.MPESA_API_URL
    headers = {
        'Authorization': f'Bearer {settings.MPESA_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'phone_number': phone_number,
        'amount': amount,
        'project_id': project_id,
        'user_id': user_id,
        'callback_url': 'https://website3-ho1y.onrender.com/payments/mpesa-callback/'
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
