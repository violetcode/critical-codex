from rest_framework import generics, permissions, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..serializers import *
from ..permissions import IsOwnerPermission

from d20.apps.core.models import Account as User
from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool
from d20.apps.resources.models import Feat, SpecialAbility, Spell

class UserList(generics.ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    paginate_by = 100

class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCharacterSheetList(generics.ListAPIView):
    lookup_field = 'username'
    serializer_class = CharacterSheetSerializer

    def get_queryset(self):
        request_user = self.request.user
        user = self.kwargs['username']

        if request_user.username == user:
            return CharacterSheet.objects.filter(player__username=user)
        else:
            return CharacterSheet.objects.filter(player__username=user).filter(is_public=True)

class CurrentUser(APIView):
    lookup_field = 'username'
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
