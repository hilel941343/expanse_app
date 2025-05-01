from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expenses import views as expenses_views

# ✅ this line was missing!

urlpatterns = [
    path('expenses/', include('expenses.urls')),
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),  # app urls (home & other views inside app)
    path('accounts/', include('django.contrib.auth.urls')),  # default auth views
    path('register/', expenses_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
