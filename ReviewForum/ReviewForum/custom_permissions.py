from rest_framework.permissions import BasePermission,SAFE_METHODS

class seller(BasePermission):
    def has_permission(self, request, view):
        return request.user.IsSeller

class customer(BasePermission):
    def has_permission(self, request, view):
        if request.user.IsSeller==False:
            return True
        return False
        
# class productowner(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.IsSeller
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.created_by==request.user