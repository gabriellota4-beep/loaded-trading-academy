from django.urls import path

from . import views

app_name = 'checkout'
urlpatterns = [
    path('course/<int:course_id>/', views.create_checkout, name='create'),
    path('success/<uuid:order_number>/', views.success, name='success'),
    path('webhook/', views.webhook, name='webhook'),
]
