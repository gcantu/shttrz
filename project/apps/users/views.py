from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from .forms import UserForm


User = get_user_model()

# Update user profile
class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm

    def get_success_url(self):
        return reverse('core:success')

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


# Change user password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('core:success')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })
