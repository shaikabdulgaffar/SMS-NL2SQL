from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True, editable=False, blank=True, null=True)
    parent_mobile = models.CharField(max_length=15, blank=True, null=True)
    student_mobile = models.CharField(max_length=15, blank=True, null=True)
    door_number = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    DAYSCHOLAR = 'dayscholar'
    HOSTELER = 'hosteler'
    SCHOLAR_TYPE_CHOICES = [
        (DAYSCHOLAR, 'Day Scholar'),
        (HOSTELER, 'Hosteler'),
    ]
    scholar_type = models.CharField(max_length=10, choices=SCHOLAR_TYPE_CHOICES, default=DAYSCHOLAR)
    hostel_block = models.CharField(max_length=50, blank=True, null=True)

    # Academic Details
    tenth_hallticket = models.CharField(max_length=30, blank=True, null=True)
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    twelfth_hallticket = models.CharField(max_length=30, blank=True, null=True)
    twelfth_branch = models.CharField(max_length=50, blank=True, null=True)
    twelfth_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    degree_hallticket = models.CharField(max_length=30, blank=True, null=True)
    degree_branch = models.CharField(max_length=50, blank=True, null=True)
    degree_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    # Present Details
    present_department = models.CharField(max_length=50, blank=True, null=True)
    present_branch = models.CharField(max_length=50, blank=True, null=True)
    present_year = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    present_semester = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    present_sem_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    # Fees
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            # Generate unique admission number
            last_id = Student.objects.all().count() + 1
            self.admission_number = f"ADM{last_id:05d}"
        if self.total_fees is not None and self.paid_fees is not None:
            self.balance = self.total_fees - self.paid_fees
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.admission_number})"