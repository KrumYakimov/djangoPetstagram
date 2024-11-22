from django.http import HttpResponseForbidden
from django.shortcuts import render


class UserIsOwnerMixin:
    """
    A mixin to check if the logged-in user is the owner of an object.
    """
    def dispatch(self, request, *args, **kwargs):
        # Ensure `get_object()` is provided by the view
        obj = self.get_object()
        if obj.user != request.user:
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)
