from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from courses.models import Category, Course
from .models import Order, OrderItem


class CheckoutTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Risk', slug='risk')
        self.course = Course.objects.create(
            category=category, title='Risk Control', slug='risk-control',
            summary='Protect capital.', description='Risk lessons.',
            level='beginner', price=Decimal('29.00'))
        self.user = get_user_model().objects.create_user(
            'buyer', email='buyer@example.com', password='safe-pass-123')

    def test_checkout_requires_login(self):
        response = self.client.post(reverse('checkout:create', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @override_settings(STRIPE_SECRET_KEY='')
    def test_missing_stripe_configuration_does_not_leave_pending_order(self):
        self.client.force_login(self.user)
        self.client.post(reverse('checkout:create', args=[self.course.id]))
        self.assertFalse(Order.objects.exists())

    def test_success_page_cannot_mark_pending_order_paid(self):
        order = Order.objects.create(
            user=self.user, email=self.user.email,
            total=self.course.price, status='pending')
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('checkout:success', args=[order.order_number]),
            {'session_id': 'cs_untrusted'})
        order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.status, 'pending')

    @override_settings(STRIPE_WEBHOOK_SECRET='whsec_test')
    @patch('checkout.views.stripe.Webhook.construct_event')
    def test_verified_paid_webhook_fulfils_matching_order(self, construct):
        order = Order.objects.create(
            user=self.user, email=self.user.email,
            total=self.course.price, status='pending',
            stripe_checkout_session='cs_test_123')
        OrderItem.objects.create(
            order=order, course=self.course, price=self.course.price)
        construct.return_value = {
            'type': 'checkout.session.completed',
            'data': {'object': {
                'id': 'cs_test_123',
                'payment_status': 'paid',
                'payment_intent': 'pi_test_123',
                'metadata': {'order_number': str(order.order_number)},
            }},
        }
        response = self.client.post(
            reverse('checkout:webhook'), data=b'{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='valid-signature')
        order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.status, 'paid')
        self.assertEqual(order.stripe_payment_intent, 'pi_test_123')

    @override_settings(STRIPE_WEBHOOK_SECRET='whsec_test')
    @patch('checkout.views.stripe.Webhook.construct_event')
    def test_webhook_does_not_fulfil_mismatched_session(self, construct):
        order = Order.objects.create(
            user=self.user, email=self.user.email,
            total=self.course.price, status='pending',
            stripe_checkout_session='cs_expected')
        construct.return_value = {
            'type': 'checkout.session.completed',
            'data': {'object': {
                'id': 'cs_different', 'payment_status': 'paid',
                'metadata': {'order_number': str(order.order_number)},
            }},
        }
        response = self.client.post(
            reverse('checkout:webhook'), data=b'{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='valid-signature')
        order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.status, 'pending')

# Create your tests here.
