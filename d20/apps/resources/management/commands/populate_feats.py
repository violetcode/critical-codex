import urllib2
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from d20.apps.resources.models import Feat

FEAT_URL = "https://sites.google.com/site/pathfindertemplate/Home/feats"

class Command(BaseCommand):
    help = 'Scrape and populate database for feats.'

    def handle(self, *args, **options):

        soup = BeautifulSoup(urllib2.urlopen(FEAT_URL).read())

        table = soup.find(id='sites-canvas-main-content').table

        for row in table.find_all('tr'):
            tds = row.find_all('td')
            try:
                name = tds[0].string
                strings = tds[2].strings
            except IndexError:
                continue

            if name == "Feat":
                #Skip title row
                continue

            name = name.replace("*", "")
            desc = ''.join(strings)

            #Add name and description to database
            feat, created = Feat.objects.update_or_create(name=name, description=desc)

            