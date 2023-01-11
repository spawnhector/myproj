from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^rest/', include("config.api_router")),
    re_path(r'^user/$',views.UserView.as_view(), name="user"),
    re_path(r'^login/$',views.LoginView.as_view(), name="login"),
    re_path(r'^register/$', views.RegisterView.as_view(), name="register"),
    re_path(r'^signals/$',views.SignalsView.as_view(), name="login"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
