from pyexpat.errors import messages
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import signup

urlpatterns = [
    path("signup/", signup, name="signup"),
]

class PasswordResetCompleteMessageView(auth_views.PasswordResetCompleteView):

    template_name = "registration/password_reset_complete.html"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Your password has been updated successfully.")
        return super().dispatch(request, *args, **kwargs)