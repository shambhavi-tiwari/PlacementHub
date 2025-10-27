from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),

    # student routes
    path('student-login/', views.student_login, name='student-login'),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('student-profile/', views.student_profile, name='student-profile'),
    path('update-student-profile/', views.update_student_profile, name='update-student-profile'),
    path('student-logout/', views.student_logout, name='student-logout'),

    # tpo routes
    path('tpo-login/', views.tpo_login, name='tpo-login'),
    path('tpo-dashboard/', views.tpo_dashboard, name='tpo-dashboard'),
    path('add-student-data/', views.add_student_data, name='add-student-data'),
    path('tpo-logout/', views.tpo_logout, name='tpo-logout'),

    # create tpo helper
    path('create-tpo/', views.create_tpo, name='create-tpo'),
]
