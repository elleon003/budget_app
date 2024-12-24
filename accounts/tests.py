from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
import pyotp

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomSignupForm, Enable2FAForm
from .models import CustomUser

class CustomUserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = self.User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Test creating a new user"""
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.two_factor_enabled)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        admin_user = self.User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_user_string_representation(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), self.user.email)

    def test_get_full_name(self):
        """Test getting user's full name"""
        self.assertEqual(self.user.get_full_name(), 'Test User')

    def test_get_short_name(self):
        """Test getting user's short name"""
        self.assertEqual(self.user.get_short_name(), 'Test')

class CustomUserFormsTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

    def test_custom_user_creation_form(self):
        """Test CustomUserCreationForm"""
        form = CustomUserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_change_form(self):
        """Test CustomUserChangeForm"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        form_data = {
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_custom_signup_form(self):
        """Test CustomSignupForm"""
        form = CustomSignupForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_enable_2fa_form(self):
        """Test Enable2FAForm"""
        form = Enable2FAForm(data={'code': '123456'})
        self.assertTrue(form.is_valid())
        
        # Test invalid code length
        form = Enable2FAForm(data={'code': '12345'})
        self.assertFalse(form.is_valid())

class CustomUserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_profile_view(self):
        """Test profile view"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_dashboard_view(self):
        """Test dashboard view"""
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_2fa_setup_view(self):
        """Test 2FA setup view"""
        response = self.client.get(reverse('accounts:2fa_setup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/2fa_setup.html')
        self.assertIn('qr_code', response.context)
        self.assertIn('form', response.context)

        # Test 2FA activation
        secret = response.context['request'].session['2fa_secret']
        totp = pyotp.TOTP(secret)
        code = totp.now()
        
        response = self.client.post(reverse('accounts:2fa_setup'), {'code': code})
        self.assertRedirects(response, reverse('accounts:profile'))
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertTrue(self.user.two_factor_enabled)

    def test_disable_2fa_view(self):
        """Test 2FA disable view"""
        # Enable 2FA first
        self.user.two_factor_enabled = True
        self.user.save()

        response = self.client.get(reverse('accounts:2fa_disable'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/2fa_disable.html')

        response = self.client.post(reverse('accounts:2fa_disable'))
        self.assertRedirects(response, reverse('accounts:profile'))
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertFalse(self.user.two_factor_enabled)

    def test_unauthenticated_access(self):
        """Test access to views when not logged in"""
        self.client.logout()
        
        # Test each protected view
        protected_urls = [
            'accounts:profile',
            'accounts:dashboard',
            'accounts:2fa_setup',
            'accounts:2fa_disable'
        ]
        
        for url in protected_urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 302)  # Should redirect to login
            self.assertIn('/accounts/login/', response.url)
