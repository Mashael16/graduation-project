# this file is a custom file where you define the Access Control rules for your API. It acts as a security layer that determines who can perform which actions beyond just being logged in.

from rest_framework.permissions import BasePermission

# self: Refers to the current permission class instance (e.g., IsManager).
#request: Contains the user's data (who is asking?) and the action (what are they doing?).
#view: Tells you which specific page or action (like create or delete) they are trying to reach.
from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow managers to create or edit objects.
    All authenticated users can read (GET).
    """
    def has_permission(self, request, view):
        # Allow read-only permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
            
        # Write permissions are only allowed to users with 'manager' role
        return request.user.is_authenticated and request.user.role == 'manager'
    
    
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employee'

