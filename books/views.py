from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
import os
import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

class InlineUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def register_view(request):
    if request.method == 'POST':
        form = InlineUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = InlineUserCreationForm()
    return render(request, 'books/register.html', {'form': form})



def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user_email, otp):
    subject = "Your Login OTP"
    message = f"Your OTP for login is: {otp}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your Login OTP'
    message = f'Your OTP for login is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # ✅ Skip OTP if user is admin (superuser or staff)
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('browse_books')  # Replace 'home' with your actual redirect view

            # ✅ Else do OTP verification
            otp = generate_otp()
            send_otp_email(user.email, otp)

            request.session['otp'] = otp
            request.session['otp_username'] = user.username
            return redirect('verify_otp')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'form': form})




def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        expected_otp = request.session.get('otp')
        username = request.session.get('otp_username')

        if entered_otp == expected_otp:
            user = User.objects.get(username=username)
            login(request, user)
            request.session.pop('otp', None)
            request.session.pop('otp_username', None)
            return redirect('browse_books')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'books/otp_verify.html')

    return render(request, 'books/otp_verify.html')



@login_required
def upload_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        age_group = request.POST['age_group']
        level = request.POST['level']
        uploaded_file = request.FILES['file']
        
        # New: Get the cover image from the uploaded files
        # Use .get() to avoid a KeyError if the user doesn't upload a cover
        cover_image = request.FILES.get('cover')

        Book.objects.create(
            title=title,
            description=description,
            age_group=age_group,
            level=level,
            file=uploaded_file,
            # New: Pass the cover image to the create method
            cover=cover_image,
        )

        return redirect('browse_books')

    return render(request, 'books/upload.html')




from django.contrib.auth.decorators import login_required

@login_required
def browse_books(request):
    age_group = request.GET.get('age_group')
    level = request.GET.get('level')
    books = Book.objects.all()
    if age_group:
        books = books.filter(age_group=age_group)
    if level:
        books = books.filter(level=level)
    return render(request, 'books/browse.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from .models import Book


# books/views.py

from .models import ReadingExercise

def exercise_list(request):
    exercises = ReadingExercise.objects.all()
    return render(request, 'books/exercise_list.html', {'exercises': exercises})

@login_required
def upload_exercise(request):
    if not request.user.is_staff:
        return redirect('browse_books')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            ReadingExercise.objects.create(title=title, content=content)
            return redirect('exercise_list')
    return render(request, 'books/upload_exercise.html')

from django.conf import settings







@login_required
def delete_book(request, book_id):
    # Use get_object_or_404 for safer retrieval
    book = get_object_or_404(Book, id=book_id)

    # Delete the associated files from AWS S3
    # This also handles cases where a file might be missing
    if book.file:
        book.file.delete()
    if book.cover:
        book.cover.delete()

    # Delete the book record from the database
    book.delete()

    return redirect('browse_books')

@login_required
def delete_exercise(request, exercise_id):
    if not request.user.is_staff:
        return redirect('browse_books')
    exercise = get_object_or_404(ReadingExercise, id=exercise_id)
    exercise.delete()
    return redirect('exercise_list')
