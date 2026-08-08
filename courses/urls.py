from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('manage/add/', views.course_create, name='create'),
    path('<slug:slug>/', views.course_detail, name='detail'),
    path('<slug:slug>/learn/', views.course_learn, name='learn'),
    path('<slug:slug>/edit/', views.course_update, name='update'),
    path('<slug:slug>/delete/', views.course_delete, name='delete'),
    path('<slug:slug>/review/', views.review_save, name='review'),
]
