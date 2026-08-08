from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import UserProfile


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=user_profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('profiles:detail')
    paid_orders = request.user.orders.filter(status='paid').prefetch_related(
        'items__course')
    enrolled_courses = [
        item.course for order in paid_orders for item in order.items.all()
    ]
    return render(request, 'profiles/profile.html', {
        'form': form,
        'orders': request.user.orders.prefetch_related('items__course'),
        'enrolled_courses': enrolled_courses,
    })

# Create your views here.
