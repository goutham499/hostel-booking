from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)  # Optional name field
    room_type = models.CharField(max_length=20)  # e.g., Single, Double, AC
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True)  # ✅ For Google Maps

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"

class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Booked')

    def __str__(self):
        return f"{self.student.username} booked Room {self.room.number}"
