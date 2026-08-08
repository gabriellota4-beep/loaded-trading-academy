from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from checkout.models import Order, OrderItem
from courses.models import Category, Course


class ProfileTests(TestCase):
    def test_profile_lists_paid_courses_in_my_learning(self):
        user = get_user_model().objects.create_user(
            'learner', password='safe-pass-123')
        category = Category.objects.create(name='Mindset', slug='mindset')
        course = Course.objects.create(
            category=category, title='Execution Discipline',
            slug='execution-discipline', summary='Build consistency.',
            description='Practical lessons.', level='beginner',
            price=Decimal('39.00'))
        order = Order.objects.create(
            user=user, email='learner@example.com', total=course.price,
            status='paid')
        OrderItem.objects.create(order=order, course=course,
                                 price=course.price)
        self.client.force_login(user)
        response = self.client.get(reverse('profiles:detail'))
        self.assertContains(response, 'My learning')
        self.assertContains(response, course.title)

# Create your tests here.
