from django.urls import path
from .views import register_view, login_view, upload_book, browse_books
from django.contrib.auth.views import LogoutView
from .views import custom_logout_view,exercise_list,upload_exercise,delete_book,delete_exercise,verify_otp_view


urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),  
    path('upload/', upload_book, name='upload_book'),
    path('browse/', browse_books, name='browse_books'),
    path('exercises/', exercise_list, name='exercise_list'),
    path('upload-exercise/', upload_exercise, name='upload_exercise'),
    path('delete/<int:book_id>/',delete_book, name='delete_book'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('delete-exercise/<int:exercise_id>/', delete_exercise, name='delete_exercise'),


]
