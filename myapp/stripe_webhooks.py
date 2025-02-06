import stripe
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
from .models import Character, PaymentStatus

import logging

# ロガーの設定
logger = logging.getLogger(__name__)

# Stripeのシークレットキーを設定
stripe.api_key = settings.STRIPE_API_KEY

@csrf_exempt
def stripe_webhook(request):
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    if request.method == 'POST':
        payload = request.body
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            logger.error(f'Invalid payload: {e}')
            return JsonResponse({'error': 'Invalid payload', 'details': str(e)}, status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f'Invalid signature: {e}')
            return JsonResponse({'error': 'Invalid signature', 'details': str(e)}, status=400)
        except Exception as e:
            logger.error(f'An error occurred: {e}', exc_info=True)
            return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)

        # イベントタイプがcheckout.session.completedの場合
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session.get('metadata', {}).get('user_id')
            try:
                user = User.objects.get(id=user_id)
                character = user.character
                # プランに応じてAPI使用回数を増やす
                line_items = stripe.checkout.Session.list_line_items(session.id, limit=10)
                for item in line_items.data:
                    # プランIDに応じた処理
                    if item.price.id == settings.MINI_PLAN_PRICE_ID:
                        character.add_api_usage_count(100)
                    elif item.price.id == settings.STANDARD_PLAN_PRICE_ID:
                        character.add_api_usage_count(500)
                    elif item.price.id == settings.DIRECTOR_PLAN_PRICE_ID:
                        character.add_api_usage_count(1100)
                
                character.save() # 忘れずに保存
                
                PaymentStatus.objects.create(user=user, status='completed')
                logger.info('Checkout session completed successfully for user_id: %s', user_id)
                return JsonResponse({'message': 'Checkout session completed successfully'}, status=200)
            except User.DoesNotExist as e:
                logger.error(f'User not found: {e} - User ID: {user_id}', exc_info=True)
                return JsonResponse({'error': 'User not found', 'details': str(e)}, status=404)
            except Exception as e:
                logger.error(f'An error occurred while processing the session: {e}', exc_info=True)
                return JsonResponse({'error': 'An error occurred while processing the session', 'details': str(e)}, status=500)
        else:
            logger.info('Unhandled event type: %s', event['type'])
            return JsonResponse({'message': 'Unhandled event type'}, status=200)
    else:
        logger.error('Method not allowed')
        return JsonResponse({'error': 'Method not allowed'}, status=405)
