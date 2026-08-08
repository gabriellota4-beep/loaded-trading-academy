import uuid

from django.conf import settings
from django.db import models

from courses.models import Course


class Order(models.Model):
    STATUS = [('pending', 'Pending'), ('paid', 'Paid'),
              ('refunded', 'Refunded')]
    order_number = models.UUIDField(default=uuid.uuid4, editable=False,
                                    unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT,
                             related_name='orders')
    email = models.EmailField()
    stripe_checkout_session = models.CharField(max_length=150, blank=True,
                                                unique=True, null=True)
    stripe_payment_intent = models.CharField(max_length=150, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS,
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.order_number)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['order', 'course'], name='unique_course_per_order')]

    def __str__(self):
        return f'{self.course} in {self.order}'

# Create your models here.
