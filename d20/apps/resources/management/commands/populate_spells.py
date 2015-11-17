import urllib2
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from d20.apps.resources.models import Spell


PAIZO_BASE_URL = "http://paizo.com/pathfinderRPG/prd/"
SPELLS_URL = "http://paizo.com/pathfinderRPG/prd/spellIndex.html"

class Command(BaseCommand):
    help = 'Scrape and populate database for spells.'

    def handle(self, *args, **options):

        soup = BeautifulSoup(urllib2.urlopen(SPELLS_URL).read())

        spells_list = soup.find(id="spell-index-wrapper")

        for letter in spells_list.find_all('ul'):
            spells = letter.find_all('li')
            for spell in spells:
                name = spell.string
                url = spell.find('a')['href']

                new_soup = BeautifulSoup(urllib2.urlopen(PAIZO_BASE_URL + url).read())
                description = new_soup.find('div', class_='body').find_all('p', recursive=False)

                desc = ""
                for d in description[1:]:
                    desc = desc + ''.join(d.strings) + "\n"

                spell, created = Spell.objects.update_or_create(name=name, description=desc)
                if created:
                    print "Created Spell: " + name
            