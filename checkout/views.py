import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from courses.models import Course
from .models import Order, OrderItem


@login_required
def create_checkout(request, course_id):
    course = get_object_or_404(Course, pk=course_id, is_published=True)
    already_owned = request.user.orders.filter(
        status='paid', items__course=course).exists()
    if already_owned:
        messages.info(request, 'You already own this course.')
        return redirect(course)
    if request.method != 'POST':
        return redirect(course)

    order = Order.objects.create(
        user=request.user, email=request.user.email, total=course.price)
    OrderItem.objects.create(order=order, course=course, price=course.price)

    if not settings.STRIPE_SECRET_KEY:
        order.delete()
        messages.error(request, 'Stripe test checkout is not configured yet.')
        return redirect(course)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    success_url = request.build_absolute_uri(reverse(
        'checkout:success', kwargs={'order_number': order.order_number}))
    session = stripe.checkout.Session.create(
        mode='payment',
        customer_email=request.user.email or None,
        line_items=[{'price_data': {
            'currency': 'gbp',
            'unit_amount': int(course.price * 100),
            'product_data': {'name': course.title},
        }, 'quantity': 1}],
        metadata={'order_number': str(order.order_number)},
        success_url=f'{success_url}?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=request.build_absolute_uri(course.get_absolute_url()),
    )
    order.stripe_checkout_session = session.id
    order.save(update_fields=['stripe_checkout_session'])
    return redirect(session.url, code=303)


@login_required
def success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number,
                              user=request.user)
    return render(request, 'checkout/success.html', {'order': order})


@csrf_exempt
@require_POST
def webhook(request):
    """Verify Stripe's signature and fulfil completed Checkout sessions."""
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=503)

    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.headers.get('Stripe-Signature', ''),
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_number = session.get('metadata', {}).get('order_number')
        if order_number and session.get('payment_status') == 'paid':
            try:
                order = Order.objects.get(
                    order_number=order_number,
                    stripe_checkout_session=session.get('id'),
                )
            except Order.DoesNotExist:
                return HttpResponse(status=200)
            order.status = 'paid'
            order.stripe_payment_intent = session.get(
                'payment_intent', '') or ''
            order.save(update_fields=['status', 'stripe_payment_intent'])

    return HttpResponse(status=200)

# Create your views here.
