from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from ..serializers import *
from ..permissions import IsOwnerPermission, IsPlayerPermission

from d20.apps.core.models import Account as User
from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool
from d20.apps.resources.models import Feat, SpecialAbility, Spell


class CharacterSheetMixin(object):
    lookup_field = 'slug'
    model = CharacterSheet
    queryset = CharacterSheet.objects.all()
    serializer_class = CharacterSheetSerializer
    permission_classes = [ permissions.IsAuthenticated, IsPlayerPermission, ]

    def pre_save(self, obj):
        """Force user to the current user on save"""
        obj.player = self.request.user
        return super(CharacterSheetMixin, self).pre_save(obj)

class CharacterSheetDetail(CharacterSheetMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

class CharacterCreate(generics.CreateAPIView):
    lookup_field = 'slug'
    model = CharacterSheet
    serializer_class = CharacterSheetSerializer
    permission_classes = [ IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)



#Lists all charactersheets that are public
class CharacterSheetList(generics.ListAPIView):
    lookup_field = 'slug'
    serializer_class = CharacterSheetSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            charsheets= CharacterSheet.objects.filter(
                Q(is_public=True) |
                Q(player__username=request_user.username)
            )
            return charsheets
        else:
            return CharacterSheet.objects.filter(is_public=True)

class WeaponMixin(object):
    lookup_field = 'slug'
    model = Weapon
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
    permission_classes = [IsAuthenticated]
    ordering = ('created',)

class WeaponDetail(WeaponMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

class WeaponCreate(generics.CreateAPIView):
    lookup_field = 'slug'
    model = Weapon
    serializer_class = WeaponSerializer
    permission_classes = [IsAuthenticated]

class SpellSchoolMixin(object):
    lookup_field = 'slug'
    model = SpellSchool
    queryset = SpellSchool.objects.all()
    serializer_class = SpellSchoolSerializer
    permission_classes = [IsAuthenticated]
    ordering = ('created',)

class SpellSchoolDetail(SpellSchoolMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

class SpellSchoolCreate(generics.CreateAPIView):
    lookup_field = 'slug'
    model = SpellSchool
    serializer_class = SpellSchoolSerializer
    permission_classes = [IsAuthenticated]

class SpellEntryMixin(object):
    model = SpellEntry
    queryset = SpellEntry.objects.all()
    serializer_class = SpellEntrySerializer
    permission_classes = [IsAuthenticated]

class SpellEntryDetail(SpellEntryMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

class SpellEntryCreate(generics.CreateAPIView):
    model = SpellEntry
    serializer_class = SpellEntrySerializer
    permission_classes = [IsAuthenticated]


