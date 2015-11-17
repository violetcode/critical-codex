from rest_framework.permissions import BasePermission

#Custom permission to only allow owners of content to view or edit it.
class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user and
            request.method in ['GET', 'PATCH', 'DELETE'])

class IsPlayerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.player == request.user and
            request.method in ['GET', 'PATCH', 'DELETE'])
