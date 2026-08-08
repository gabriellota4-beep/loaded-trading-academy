from django import forms

from .models import Course, Review


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category', 'title', 'slug', 'summary', 'description',
                  'learning_outcomes', 'lesson_content', 'level', 'price',
                  'is_published']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})}
