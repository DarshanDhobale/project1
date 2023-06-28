from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# class CustomLoginView(auth_views.LoginView):
#     def get_success_url(self):
#         return 'problems'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('problems/', views.problems, name='problems'),
    path('problems/<int:problem_id>/', views.problem_description, name='problem_description'),
    path('problems/<int:problem_id>/compile/', views.compile_code, name='compile_code'),
]