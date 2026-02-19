# this file is a custom file where you define the Access Control rules for your API. It acts as a security layer that determines who can perform which actions beyond just being logged in.

from rest_framework.permissions import BasePermission

# self: Refers to the current permission class instance (e.g., IsManager).
#request: Contains the user's data (who is asking?) and the action (what are they doing?).
#view: Tells you which specific page or action (like create or delete) they are trying to reach.
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employee'

