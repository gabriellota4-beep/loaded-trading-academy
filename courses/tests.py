from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from checkout.models import Order, OrderItem
from .models import Category, Course, Review


class CourseViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Structure', slug='structure')
        self.course = Course.objects.create(
            category=self.category, title='Code 4 Foundations',
            slug='code-4-foundations', summary='Read market structure.',
            description='A practical course.', level='beginner',
            price=Decimal('49.00'))
        self.user = get_user_model().objects.create_user('dada', password='safe-pass-123')

    def test_course_list_and_detail_are_public(self):
        self.assertContains(self.client.get(reverse('courses:list')), self.course.title)
        self.assertContains(self.client.get(self.course.get_absolute_url()), self.course.summary)

    def test_regular_user_cannot_access_course_management(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('courses:create'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_review(self):
        order = Order.objects.create(
            user=self.user, email='dada@example.com',
            total=self.course.price, status='paid')
        OrderItem.objects.create(
            order=order, course=self.course, price=self.course.price)
        self.client.force_login(self.user)
        self.client.post(reverse('courses:review', args=[self.course.slug]),
                         {'rating': 5, 'comment': 'Clear and useful.'})
        self.assertTrue(Review.objects.filter(author=self.user,
                                              course=self.course).exists())

    def test_user_without_purchase_cannot_open_lesson_or_review(self):
        self.client.force_login(self.user)
        lesson = self.client.get(reverse('courses:learn', args=[self.course.slug]))
        self.assertRedirects(lesson, self.course.get_absolute_url())
        self.client.post(reverse('courses:review', args=[self.course.slug]),
                         {'rating': 5, 'comment': 'Should not save.'})
        self.assertFalse(Review.objects.filter(author=self.user).exists())

    def test_paid_user_can_open_lesson(self):
        order = Order.objects.create(
            user=self.user, email='dada@example.com',
            total=self.course.price, status='paid')
        OrderItem.objects.create(
            order=order, course=self.course, price=self.course.price)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('courses:learn', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)

# Create your tests here.
