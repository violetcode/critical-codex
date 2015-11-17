from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..serializers import *
from ..permissions import IsOwnerPermission

from d20.apps.core.models import Account as User
from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool
from d20.apps.resources.models import Feat, SpecialAbility, Spell


class SpecialAbilitiesList(generics.ListAPIView):
    queryset =SpecialAbility.objects.all()
    serializer_class = SpecialAbilitySerializer
    permission_classes = (permissions.AllowAny, )
    paginate_by = 100

class SpellsList(generics.ListAPIView):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer
    permission_classes = (permissions.AllowAny, )
    paginate_by = 700

class FeatsList(generics.ListAPIView):
    queryset = Feat.objects.all()
    serializer_class = FeatSerializer
    permission_classes = (permissions.AllowAny, )
    paginate_by = 400
