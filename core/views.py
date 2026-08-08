from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from courses.models import Course
from .forms import RegistrationForm


def home(request):
    featured = Course.objects.filter(is_published=True)[:3]
    return render(request, 'core/home.html', {'featured_courses': featured})


def register(request):
    if request.user.is_authenticated:
        return redirect('courses:list')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Welcome to Loaded Trading Academy.')
        return redirect('profiles:detail')
    return render(request, 'registration/register.html', {'form': form})


def about(request):
    return render(request, 'core/about.html')

# Create your views here.
