from django import forms
from django.forms import widgets, Select
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib import messages

from zebra.forms import StripePaymentForm
from .models import Account


PLANS = [
    ("criticalcodex-12", mark_safe("$12 - Premium Account")),
    ("criticalcodex-24", mark_safe("$24 - I'm Feeling Generous")),
]

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            choices = '\n'.join(['%s\n' % w for w in self])
            return mark_safe('%s' % choices)

class StripePlusPaymentForm(StripePaymentForm):
    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email')
        plan = kwargs.pop('plan', '')
        super(StripePlusPaymentForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = email
        if plan:
            self.fields['plan'].initial = plan

	card_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}), label='Credit card number')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control',}), label='Email address', required=False)
    plan = forms.ChoiceField(required=False, widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=PLANS, label='Plan')

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': _("Enter your username")}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _("Enter password")}),
    )

    #Code for upcoming 1.7
    def confirm_login_allowed(self, user):
        if not user.is_active:
            #user.reactivate_account()
            #messages.success(request, 'Your account has been reactivated.')
            pass

    #hack for django 1.6
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                #self.user_cache.reactivate_account()
                #messages.success(request, 'Your account has been reactivated.')
                #reactivated_account = True
                pass
        return self.cleaned_data

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Enter your email address to reset your password"),
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email',}),
        max_length=254,
    )

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()

        # Find users of this email address
        UserModel = get_user_model()
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_("Please fill your email address."))
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)

        if active_users.exists():
            # Check if all users of the email address are LDAP users (and give an error if they are)
            found_non_ldap_user = False
            for user in active_users:
                if user.has_usable_password():
                    found_non_ldap_user = True
                    break

            if not found_non_ldap_user:
                # All found users are LDAP users, give error message
                raise forms.ValidationError(_("Sorry, you cannot reset your password here as your user account is managed by another server."))
        else:
            # No user accounts exist
            raise forms.ValidationError(_("This email address is not recognised."))

        return cleaned_data


class AccountForm(forms.ModelForm):
    #Assumes that the Account instance passed in has an associated User
    #object. The view (see views.py) takes care of that
    class Meta(object):
        model = Account
        fields = ['about', 'location', 'url', 'gender', ]
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {}).update({'email': instance.email})
        super(AccountForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AccountForm, self).save(commit=commit)
        if 'email' in self.cleaned_data:
            instance.email = self.cleaned_data['email']
            if commit:
                instance.save()
        return instance


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }
    username = forms.RegexField(
    	label=_("Username"),
    	widget=forms.TextInput(attrs={'type':'text', 'class':'form-control', 'placeholder':'Username',}),
    	max_length=30,
    	regex=r'^[\w-]+$',
    	error_message = _("Usernames must contain only letters, numbers and underscores.")
    )
    password = forms.CharField(
    	label=_("Password"),
    	widget=forms.PasswordInput(attrs={'type':'password', 'class':'form-control', 'placeholder':'Password',})
    )
    email = forms.CharField(
    	label=_("Email"),
    	widget=forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email',})
    )

    class Meta:
        model = Account
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        username = self.cleaned_data["username"]
        try:
            Account._default_manager.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SiteSettingsForm(forms.ModelForm):

	class Meta:
		model = Account
		exclude = (
			'username', 'email', 'timezone', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
			'hide_mobile', 'last_seen_on', 'last_seen_ip', 'preferences', 'view_settings', 'cname', 'slug',
			'is_premium', 'premium_expire', 'secret_token', 'stripe_4_digits', 'stripe_id',

            'first_name', 'last_name', 'about', 'location', 'url', 'gender', 'image', 'send_emails',
			)
		widgets = {
			'feed_column_size': forms.Select(attrs={'class':'form-control',}),
			'feed_size': forms.Select(attrs={'class':'form-control',}),
			'is_beta': forms.RadioSelect,
		}

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = (
            'username', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
            'hide_mobile', 'last_seen_on', 'last_seen_ip', 'preferences', 'view_settings', 'cname', 'slug',
            'is_premium', 'premium_expire', 'secret_token', 'stripe_4_digits', 'stripe_id',
            'feed_column_size', 'feed_size', 'timezone', 'send_emails', 'is_beta', 'email',
            )

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name',}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name',}),
            'about': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Brief bio', 'rows':'2'}),
            'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location',}),
            'url': forms.TextInput(attrs={'type':'url', 'class':'form-control', 'placeholder':'Link to your other website?',}),
            'gender': forms.Select(attrs={'class':'form-control',}),
            'image': forms.FileInput,
        }


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = (
            'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
            'hide_mobile', 'last_seen_on', 'last_seen_ip', 'preferences', 'view_settings', 'cname', 'slug',
            'is_premium', 'premium_expire', 'secret_token', 'stripe_4_digits', 'stripe_id',
            'first_name', 'last_name', 'about', 'location', 'url', 'gender', 'image',
            'feed_column_size', 'feed_size', 'is_beta',
            )

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username',}),
            'email': forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email address',}),
            'timezone': forms.Select(attrs={'class':'form-control',}),
            'send_emails': forms.RadioSelect,
        }
