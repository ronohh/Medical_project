from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER = (
        (1, 'admin'),
        (2, 'doctor'),
        (3, 'patient'),
        (4, 'staff' ),
    )
    user_type = models.IntegerField(choices=USER, default=1)

    mobilenumber = models.CharField(max_length=13, unique=True, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True)

    def __str__(self):
        return self.username


class DoctorRegistration(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    regdate_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"user not associated - {self.mobilenumber}"
 
class PatientReg(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=100)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    appointmentnumber = models.IntegerField(default=0)
    pat_id = models.ForeignKey(PatientReg, on_delete=models.CASCADE)
    date_of_appointment = models.CharField(max_length= 250)
    time_of_appointment = models.CharField(max_length= 250)
    doctor_id = models.ForeignKey(DoctorRegistration, on_delete=models.CASCADE)
    additional_msg = models.TextField(blank= True)
    diagnosis = models.CharField(max_length= 250, default="")
    prescription = models.CharField(max_length=250, default="")
    status = models.CharField(default=0, max_length=200)
    consultancy_fee = models.DecimalField(max_digits=5, decimal_places=2,default=100)
    paid_by_insurance = models.BooleanField(default=False)

    def save(self,*args, **kwargs):
        # is_new = self._state.adding
        super().save(*args, **kwargs)
        # if is_new:
        #     try:
        #         insurance = Insurance.objects.get(patient=self.pat_id)
        #         if insurance.deduct_fee(self.consultancy_fee):
        #             self.paid_by_insurance = True
        #             super().save(update_fields=["paid_by_insurance"])
        #     except Insurance.DoesNotExist:
        #         pass
    @property
    def is_paid(self):
        if self.paid_by_insurance:
            return True
        last_payment = (
            self.payments.order_by("-created_at").first()
            if hasattr(self, "payments") else None
        )
        return last_payment and last_payment.status == "success"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hospital(models.Model):
    hname = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.hname

class ReferralAppointment(models.Model):
    referralnumber = models.IntegerField(default=0)
    pat_id = models.ForeignKey(PatientReg, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date_of_referral = models.CharField(max_length=250)
    time_of_referral = models.CharField(max_length=250)
    doctor_id = models.ForeignKey(DoctorRegistration, on_delete=models.CASCADE)
    additional_msg =models.TextField(blank= True)
    remark = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20,choices=[("Pending","Pending"),("Accepted","Accepted"),("Rejected","Rejected")], default="Pending")

    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    

class AddPatient(models.Model):
    doctor_id = models.ForeignKey(DoctorRegistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobilenumber = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=100)
    medicalhistory = models.TextField(max_length= 10)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class MedicalHistory(models.Model):
    pat_id = models.ForeignKey(AddPatient, on_delete=models.CASCADE, related_name='medical_histories', default=0 )
    bloodpressure = models.CharField(max_length=250)
    weight = models.CharField(max_length=250)
    bodytemp =models.CharField(max_length=250)
    diagnosis = models.CharField(max_length= 250)
    prescription = models.TextField()
    visitingdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    appointment =models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank = True, related_name='payments')
    patient = models.ForeignKey(PatientReg, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=13)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_code = models.CharField(max_length= 20, blank= True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10,choices=[("pending","Pending"),("success","Success"),("failed","Failed")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

class Insurance(models.Model):
    patient = models.OneToOneField(PatientReg, on_delete=models.CASCADE)
    total_cover = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)

    def deduct_fee(self,amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
    def __str__(self):
        return f"{self.patient.admin.first_name} {self.patient.admin.last_name} Insurance Balance: {self.balance}"
    