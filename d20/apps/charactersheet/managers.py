import datetime
import markdown

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

class CharactersheetManager(models.Manager):

	def public(self):
		return super(CharactersheetManager, self).get_query_set().filter(is_public=True)
