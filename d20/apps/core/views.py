import hashlib
import json
import stripe

from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import cache
from django.template import RequestContext

from .forms import AccountForm, ProfileForm, SiteSettingsForm, UserCreationForm, PLANS, StripePlusPaymentForm
from .models import Account

def register(request):
    if not settings.ALLOW_NEW_REGISTRATIONS:
        messages.error(request, "The admin of this service is not allowing new registrations.")
        return redirect(settings.SITE_URL)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return redirect(settings.SITE_URL)
    else:
        form = UserCreationForm()

    return TemplateResponse(request, 'core/register.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect(settings.SITE_URL)

@login_required
def EditAccount(request):
	account = get_object_or_404(Account, username=request.user)
	f = AccountForm(request.POST or None, instance=account)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Changes saved.')
		return redirect('Core:AccountSettings')
	variables = RequestContext(request, {'form': f, 'user_obj': account,})
	return render_to_response('core/account/settings.html', variables)

@login_required
def EditProfile(request):
    account = get_object_or_404(Account, username=request.user)
    f = ProfileForm(request.POST or None, instance=account)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'Changes saved.')
        return redirect('Core:ProfileSettings')
    variables = RequestContext(request, {'form': f, 'user_obj': account,})
    return render_to_response('core/account/profile.html', variables)

@login_required
def EditPremium(request):
    account = get_object_or_404(Account, username=request.user)
    f = SiteSettingsForm(request.POST or None, instance=account)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'Changes saved.')
        return redirect('Core:PremiumSettings')
    variables = RequestContext(request, {'form': f, 'user_obj': account,})
    return render_to_response('core/account/premium.html', variables)

@login_required
def CancelPremium(request):
    account = get_object_or_404(Account, username=request.user)
    if request.method == 'POST':
        account.cancel_premium()
        messages.success(request, 'You have canceled your premium membership.')
        return redirect('Core:SiteSettings')
    return render(request, 'core/account/premium_deactivation.html', {'user_obj': account,})

@login_required
def stripe_form(request):
    user = request.user
    success_updating = False
    stripe.api_key = settings.STRIPE_SECRET
    plan = int(request.GET.get('plan', 2))
    plan = PLANS[plan-1][0]
    error = None

    if request.method == 'POST':
        zebra_form = StripePlusPaymentForm(request.POST, email=user.email)
        if zebra_form.is_valid():
            user.email = zebra_form.cleaned_data['email']
            user.save()

            try:
                customer = stripe.Customer.create(**{
                    'card': zebra_form.cleaned_data['stripe_token'],
                    'plan': zebra_form.cleaned_data['plan'],
                    'email': user.email,
                    'description': user.username,
                })
            except stripe.CardError:
                error = "This card was declined."
            else:
                user.strip_4_digits = zebra_form.cleaned_data['last_4_digits']
                user.stripe_id = customer.id
                user.save()
                user.activate_premium() # TODO: Remove, because webhooks are slow

                success_updating = True

    else:
        zebra_form = StripePlusPaymentForm(email=user.email, plan=plan)

    if success_updating:
        return render_to_response('core/stripe_success.html',
                                  {}, context_instance=RequestContext(request))

    return render_to_response('core/stripe_form.html',
        {
          'zebra_form': zebra_form,
          'publishable': settings.STRIPE_PUBLISHABLE,
          'success_updating': success_updating,
          'error': error,
        },
        context_instance=RequestContext(request)
    )

@login_required
def stripe_success(request):
    return TemplateResponse(request, 'core/stripe_success.html', {})

@login_required
def deactivate_account(request):
    account = get_object_or_404(Account, username=request.user)
    if request.method == 'POST':
        account.deactivate_account()
        logout(request)
        messages.success(request, 'Your account is now pending deletion. To cancel, log back in and follow the directions on screen.')
        return redirect(settings.SITE_URL)
    return render(request, 'core/account/confirm_deactivation.html', {'user_obj': account,})

@login_required
def reactivate_account(request):
    account = get_object_or_404(Account, username=request.user)
    if request.method == 'POST':
        account.reactivate_account()
        messages.success(request, 'You have reactivated_account!')
        return redirect(settings.SITE_URL)
    return render(request, 'core/account/confirm_reactivation.html', {'user_obj': account,})
