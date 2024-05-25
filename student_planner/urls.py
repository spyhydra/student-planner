from django.contrib import admin
from django.urls import path

from time_planner.views import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('add-task/', views.add_and_show_tasks, name='add-task'),
    path('task/', views.show_tasks, name='task'),

    path('delete-task/<int:id>', views.delete_task, name='delete-task'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('complete-task/<int:id>', views.complete_task, name='complete_task'),
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),




]
