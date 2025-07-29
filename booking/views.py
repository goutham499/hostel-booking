from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # ✅ For email sending

# ✅ Home view: display all rooms
def home(request):
    rooms = Room.objects.all()
    return render(request, 'booking/home.html', {'rooms': rooms})

# ✅ Register new users
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

# ✅ Book a room
@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if room.is_available:
        Booking.objects.create(student=request.user, room=room)
        room.is_available = False
        room.save()

        # ✅ Send confirmation email
        send_mail(
            'Room Booking Confirmation',
            f'Hi {request.user.username}, your booking for room "{room.name}" is confirmed.',
            'your_email@gmail.com',  # ⚠️ Replace this with your real sender email
            [request.user.email],
            fail_silently=True,  # Set to False during development to debug email issues
        )

        # ✅ Add success message
        messages.success(request, f'Room "{room.name}" booked successfully! Confirmation email sent.')
    else:
        messages.warning(request, 'Sorry, this room is already booked.')

    return redirect('my_bookings')

# ✅ View your bookings
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(student=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

# ✅ Cancel a booking
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    room = booking.room
    booking.delete()
    room.is_available = True
    room.save()

    # ✅ Add cancel message
    messages.warning(request, f'Your booking for room "{room.name}" has been cancelled.')

    return redirect('my_bookings')
