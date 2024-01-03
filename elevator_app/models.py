from django.db import models

# Create your models here.

# First create a Model for Building,


class Elevator(models.Model):
    name = models.CharField(max_length=200)
    max_floor = models.IntegerField(null=False)
    min_floor = models.IntegerField(null=False)
    current_floor = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    door_status = models.BooleanField(default=False)
    running_direction = models.BooleanField(default=False)
    running_status = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ElevatorRequest(models.Model):
    requested_from_floor = models.IntegerField()
    requested_floor = models.IntegerField(null=True)
    status = models.BooleanField(default=False)
    is_fullfilled = models.BooleanField(default=False)
    requested_date_time = models.DateTimeField(auto_now_add=True)
    full_filled_date_time = models.DateTimeField(auto_now=True)
    full_filled_by = models.ForeignKey(
        Elevator, related_name="elevatorrequests", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f"Requested from Floor: {self.requested_from_floor} to floor: {self.requested_floor} and Elevator is: {self.full_filled_by}"
