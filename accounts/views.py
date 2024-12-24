from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, TemplateView
from django.utils.translation import gettext_lazy as _
import pyotp

from .forms import CustomUserChangeForm, Enable2FAForm
from .models import CustomUser

class ProfileView(LoginRequiredMixin, UpdateView):
    """View for updating user profile information."""
    
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, _('Your profile has been updated successfully.'))
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TwoFactorSetupView(TemplateView):
    """View for setting up 2FA."""
    
    template_name = 'accounts/2fa_setup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.session.get('2fa_secret'):
            # Generate new secret key
            secret = pyotp.random_base32()
            self.request.session['2fa_secret'] = secret
            
            # Generate QR code
            totp = pyotp.TOTP(secret)
            context['qr_code'] = totp.provisioning_uri(
                self.request.user.email,
                issuer_name="Budget App"
            )
            
        context['form'] = Enable2FAForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = Enable2FAForm(request.POST)
        if form.is_valid():
            secret = request.session.get('2fa_secret')
            if not secret:
                messages.error(request, _('Session expired. Please try again.'))
                return redirect('2fa_setup')
            
            # Verify the code
            totp = pyotp.TOTP(secret)
            if totp.verify(form.cleaned_data['code']):
                # Enable 2FA for the user
                request.user.two_factor_enabled = True
                request.user.save()
                
                # Clean up session
                del request.session['2fa_secret']
                
                messages.success(request, _('Two-factor authentication has been enabled.'))
                return redirect('profile')
            else:
                messages.error(request, _('Invalid verification code. Please try again.'))
        
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def disable_2fa(request):
    """View for disabling 2FA."""
    if request.method == 'POST':
        request.user.two_factor_enabled = False
        request.user.save()
        messages.success(request, _('Two-factor authentication has been disabled.'))
        return redirect('profile')
    return render(request, 'accounts/2fa_disable.html')

@login_required
def dashboard(request):
    """User dashboard view."""
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })
