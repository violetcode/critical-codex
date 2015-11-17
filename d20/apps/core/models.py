import datetime
import stripe
from hashlib import md5
from cStringIO import StringIO
from PIL import Image

from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

from zebra.signals import zebra_webhook_customer_subscription_created
from zebra.signals import zebra_webhook_charge_succeeded

from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool
from d20.apps.resources.models import Feat, SpecialAbility, Spell

from timezone_field import TimeZoneField
from d20.utils.user_functions import generate_secret_token

GENDER_CHOICES = (
	('F', _('Female')),
	('M', _('Male')),
	('P', _('Pirate')),
	('N', _('Ninja')),
	('R', _('Robot')),
	('O', _('Other')),
)

COLUMN_SIZE = (
	(0, _('News Stream (Beta)')),
	(1, _('1 Column - Classic')),
	(2, _('2 Column - Classic')),
	(3, _('3 Column - Classic')),
	(4, _('3 - Default')),
)

FEED_SIZE = (
	(3, _('3')),
	(5, _('5 - Default')),
	(8, _('8')),
)

IS_BETA_CHOICES = ((True, 'Enabled'), (False, 'Disabled'))

def upload_profile_img(instance, filename):
	ext = filename.split('.')[-1]
	f_base = "%s" % (instance.id)
	f_encoded = uid_base.encode('ascii', 'ignore')
	f_name = md5(uid_encoded).hexdigest()[:24]
	filename = "%s.%s" % ('cover', ext)
	return 'user_uploads/profile/%s/%s' % (f_name, filename)

def upload_profile_img_thumb(instance, filename):
	ext = filename.split('.')[-1]
	f_base = "%s" % (instance.id)
	f_encoded = f_base.encode('ascii', 'ignore')
	f_name = md5(f_encoded).hexdigest()[:24]
	filename = "%s.%s" % ('cover_small', ext)
	return 'user_uploads/user/%s/%s' % (f_name, filename)

def validate_image(fieldfile_obj):
	filesize = fieldfile_obj.file.size
	megabyte_limit = 2.0
	if filesize > megabyte_limit*1024*1024:
		raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class Account(AbstractUser):

	#Profile Settings
	about = models.TextField(blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	location = models.CharField(max_length=255, blank=True)
	url = models.URLField(max_length=500, blank=True)
	image = models.ImageField(upload_to=upload_profile_img, validators=[validate_image], blank=True, null=True)

	#Settings
	hide_mobile = models.BooleanField(default=False)
	last_seen_on = models.DateTimeField(default=datetime.datetime.now)
	last_seen_ip = models.CharField(max_length=50, blank=True, null=True)
	preferences = models.TextField(default="{}")
	view_settings = models.TextField(default="{}")
	send_emails = models.BooleanField(choices=IS_BETA_CHOICES, default=False)
	is_beta = models.BooleanField(choices=IS_BETA_CHOICES, default=False)
	feed_size = models.IntegerField(choices=FEED_SIZE, default=5)
	feed_column_size = models.IntegerField(choices=COLUMN_SIZE, default=3)
	timezone = TimeZoneField(default="US/Pacific")

	is_premium = models.BooleanField(default=False)
	premium_expire = models.DateTimeField(blank=True, null=True)
	stripe_4_digits = models.CharField(max_length=4, blank=True, null=True)
	stripe_id = models.CharField(max_length=24, blank=True, null=True)
	secret_token = models.CharField(max_length=12, blank=True, null=True)

	class Meta:
		db_table = 'Account'

	def get_absolute_url(self):
		return "/user/%s/" % (self.username)

	def character_count(self):
		item_counts = CharacterSheet.objects.filter(player=self).count()
		return item_counts

	def save(self, *args, **kwargs):
		if not self.secret_token:
			self.secret_token = generate_secret_token(self.username, 12)
		super(Account, self).save(*args, **kwargs)

	def activate_premium(self):
		self.is_premium = True
		self.is_active = True
		self.save()
		self.setup_premium_history()
		return True

	def deactivate_premium(self):
		self.is_premium = False
		self.save()

	def deactivate_account(self):
		self.is_active = False
		if self.is_premium:
			self.cancel_premium_stripe()
		self.save()
		return True

	def reactivate_account(self):
		self.is_active = True
		self.save()
		return True

	def cancel_premium(self):
		stripe_cancel = self.cancel_premium_stripe()
		return stripe_cancel

	def cancel_premium_stripe(self):
		if not self.stripe_id:
			return
		stripe.api_key = settings.STRIPE_SECRET
		stripe_customer = stripe.Customer.retrieve(self.stripe_id)
		try:
			stripe_customer.cancel_subscription()
		except stripe.InvalidRequestError:
			logging.user(self.user, "~FRFailed to cancel Stripe subscription")
		return True

	def setup_premium_history(self, alt_email=None):
		existing_history = PaymentHistory.objects.filter(user=self)
		if existing_history.count():
			print " ---> Deleting existing history: %s payments" % existing_history.count()
			existing_history.delete()

		# Record Stripe payments
		if self.stripe_id:
			stripe.api_key = settings.STRIPE_SECRET
			stripe_customer = stripe.Customer.retrieve(self.stripe_id)
			stripe_payments = stripe.Charge.all(customer=stripe_customer.id).data

			existing_history = PaymentHistory.objects.filter(user=self,
															 payment_provider='stripe')
			if existing_history.count():
				print " ---> Deleting existing history: %s stripe payments" % existing_history.count()
				existing_history.delete()

			for payment in stripe_payments:
				created = datetime.datetime.fromtimestamp(payment.created)
				PaymentHistory.objects.create(user=self,
											  payment_date=created,
											  payment_amount=payment.amount / 100.0,
											  payment_provider='stripe')
			print " ---> Found %s stripe_payments" % len(stripe_payments)

		# Calculate payments in last year, then add together
		payment_history = PaymentHistory.objects.filter(user=self)
		last_year = datetime.datetime.now() - datetime.timedelta(days=364)
		recent_payments_count = 0
		oldest_recent_payment_date = None
		for payment in payment_history:
			if payment.payment_date > last_year:
				recent_payments_count += 1
				if not oldest_recent_payment_date or payment.payment_date < oldest_recent_payment_date:
					oldest_recent_payment_date = payment.payment_date
		print " ---> %s payments" % len(payment_history)

		if oldest_recent_payment_date:
			self.premium_expire = (oldest_recent_payment_date +
								   datetime.timedelta(days=365*recent_payments_count))
			self.save()





class PaymentHistory(models.Model):
	user = models.ForeignKey(Account, related_name='payments')
	payment_date = models.DateTimeField()
	payment_amount = models.IntegerField()
	payment_provider = models.CharField(max_length=20)

	def __unicode__(self):
		return "[%s] $%s/%s" % (self.payment_date.strftime("%Y-%m-%d"), self.payment_amount,
								self.payment_provider)
	class Meta:
		ordering = ['-payment_date']

	def canonical(self):
		return {
			'payment_date': self.payment_date.strftime('%Y-%m-%d'),
			'payment_amount': self.payment_amount,
			'payment_provider': self.payment_provider,
		}

	@classmethod
	def report(cls, months=12):
		total = cls.objects.all().aggregate(sum=Sum('payment_amount'))
		print "Total: $%s" % total['sum']

		for m in range(months):
			now = datetime.datetime.now()
			start_date = now - datetime.timedelta(days=(m+1)*30)
			end_date = now - datetime.timedelta(days=m*30)
			payments = cls.objects.filter(payment_date__gte=start_date, payment_date__lte=end_date)
			payments = payments.aggregate(avg=Avg('payment_amount'),
										  sum=Sum('payment_amount'),
										  count=Count('user'))
			print "%s months ago: avg=$%s sum=$%s users=%s" % (
				m, payments['avg'], payments['sum'], payments['count'])
