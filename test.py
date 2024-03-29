#!/usr/bin/env python3
from datetime import datetime

from schedule import Schedule, Appointment


# tests
# Implement an API to create an appointment, rejecting it if there's a conflict.
# Implement an API to get all appointments within a time window for a specified doctor.
# Implement an API to get the first available appointment after a specified time
#  i.e. I'm a patient and I'm looking for the first available appointment


test_sched = Schedule('noah', 8, 4)

print(f'Created schedule: {test_sched.schedule}')

test_sched.create_appointment('2023-08-24', '9:00', '10:30')
test_sched.create_appointment('2023-08-24', '10:45', '11:30')
test_sched.create_appointment('2023-08-25', '12:45', '14:30')

print(f'Added to schedule: {test_sched.schedule}')

assert(len(test_sched.schedule) == 3)


appt1 = Appointment(datetime(2023, 8, 24, 9, 30), datetime(2023, 8, 24, 10, 15))
appt2 = Appointment(datetime(2023, 8, 24, 10, 0), datetime(2023, 8, 24, 11, 30))
assert(test_sched._is_conflict(appt1, appt2))

appt3 = Appointment(datetime(2023, 8, 24, 9, 30), datetime(2023, 8, 24, 10, 15))
appt4 = Appointment(datetime(2023, 8, 24, 10, 15), datetime(2023, 8, 24, 11, 30))
assert(not test_sched._is_conflict(appt3, appt4))

appt5 = Appointment(datetime(2023, 8, 24, 9, 30), datetime(2023, 8, 24, 10, 15))
appt6 = Appointment(datetime(2023, 8, 24, 11, 15), datetime(2023, 8, 24, 11, 30))
assert(not test_sched._is_conflict(appt5, appt6))

appts_in_window = test_sched.get_appointments('2023-08-24', '08:00', '19:00')
print(appts_in_window)

first_appt = test_sched.get_first_appointment('2023-08-24', '20:00')
print(first_appt)
