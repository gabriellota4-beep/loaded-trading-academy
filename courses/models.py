from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVELS = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
              ('advanced', 'Advanced')]
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='courses')
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=150, unique=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    learning_outcomes = models.TextField(
        help_text='Enter one learning outcome per line.', blank=True)
    lesson_content = models.TextField(
        help_text='Course material visible only to enrolled learners.',
        blank=True)
    level = models.CharField(max_length=20, choices=LEVELS)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def user_has_access(self, user):
        """Return whether a user may open this course's private lesson."""
        if not user.is_authenticated:
            return False
        return user.is_staff or user.orders.filter(
            status='paid', items__course=self
        ).exists()


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='course_reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['course', 'author'], name='one_review_per_course_user')]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course}: {self.rating}/5 by {self.author}'

# Create your models here.
