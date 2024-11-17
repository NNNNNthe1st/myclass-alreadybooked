#this update might be necessary on views.py, please check for what is needed.
# views.py

from django.shortcuts import render, redirect
from .models import TimeSlot, Booking
from django.contrib.auth.decorators import login_required

@login_required
def book_class(request, slot_id):
    slot = TimeSlot.objects.get(id=slot_id)
    user = request.user

    # Check if the user has already booked this slot
    existing_booking = Booking.objects.filter(user=user, time_slot=slot).exists()

    if existing_booking:
        # If already booked, render the 'already_booked.html' template with context
        return render(request, 'already_booked.html', {'already_booked': True, 'slot': slot})

    # Proceed with booking if the slot is available
    if slot.is_available:
        # Create a new booking and mark the slot as unavailable
        booking = Booking.objects.create(user=user, time_slot=slot)
        slot.is_available = False
        slot.save()

        # Redirect to booking success page
        return redirect('booking_success')

    # If the slot is not available, show the 'already_booked.html' template with context
    return render(request, 'already_booked.html', {'already_booked': False, 'slot': slot})
