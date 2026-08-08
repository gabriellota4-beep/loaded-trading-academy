from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, ReviewForm
from .models import Course, Review


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        courses = courses.filter(Q(title__icontains=query) |
                                 Q(summary__icontains=query))
    return render(request, 'courses/course_list.html',
                  {'courses': courses, 'query': query})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'has_access': course.user_has_access(request.user),
        'review_form': ReviewForm(),
    })


@login_required
def course_learn(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if not course.user_has_access(request.user):
        messages.error(request, 'Purchase this course to open its lessons.')
        return redirect(course)
    return render(request, 'courses/course_learn.html', {'course': course})


@user_passes_test(lambda user: user.is_staff)
def course_create(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        course = form.save()
        messages.success(request, 'Course created successfully.')
        return redirect(course)
    return render(request, 'courses/course_form.html', {'form': form})


@user_passes_test(lambda user: user.is_staff)
def course_update(request, slug):
    course = get_object_or_404(Course, slug=slug)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Course updated successfully.')
        return redirect(course)
    return render(request, 'courses/course_form.html', {'form': form})


@user_passes_test(lambda user: user.is_staff)
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('courses:list')
    return render(request, 'courses/course_confirm_delete.html',
                  {'course': course})


@login_required
def review_save(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if not course.user_has_access(request.user):
        messages.error(request, 'Only enrolled learners can review a course.')
        return redirect(course)
    review = Review.objects.filter(course=course, author=request.user).first()
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        saved = form.save(commit=False)
        saved.course, saved.author = course, request.user
        saved.save()
        messages.success(request, 'Your review has been saved.')
    else:
        messages.error(request, 'Please correct the review form.')
    return redirect(course)

# Create your views here.
