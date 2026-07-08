from django.db import models
from schools.models import School
from accounts.models import StudentProfile

class Bus(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Bus {self.bus_number}"

class Driver(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Route(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "North Route A"
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()
    arrival_time = models.TimeField(help_text="Estimated time of arrival at this stop")
    sequence_order = models.IntegerField(default=1)

    class Meta:
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.name} ({self.route.name})"

class StudentBusAssignment(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='bus_assignment')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.user.username} -> Route: {self.route.name} (Stop: {self.stop.name})"

class BusLocationLog(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='location_logs')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bus {self.bus.bus_number} at ({self.latitude}, {self.longitude}) @ {self.timestamp}"
