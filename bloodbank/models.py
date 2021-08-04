from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BRequests(models.Model):
  status_choices=(
    (0,'pending'),
    (1,'approve'),
    (2,'done'),
    )
  blood_choices=(
    ("O Positive","O Positive"),
    ("O Negative","O Negative"),
    ("A Positive","A Positive"),
    ("A Negative","A Negative"),
    ("B Positive","B Positive"),
    ("B Negative","B Negative"),
    ("AB Positive","AB Positive"),
    ("AB Negative","AB Negative"),
    )
  patient_name=models.CharField(max_length=100)
  attendant_name=models.CharField(max_length=100)
  contact_number=models.CharField(max_length=15)
  blood_group=models.CharField(max_length=50,choices=blood_choices)
  quantity=models.IntegerField(null=True, blank=True)
  hospital_name=models.CharField(max_length=100)
  deadline=models.DateField()
  status=models.IntegerField(choices=status_choices)
  the_donors=models.TextField(max_length=700,default="none")


  def __str__(self):
    return self.patient_name
  

class Donors(models.Model):
  gender_choices=(
    ("Male","Male"),
    ("Female","Female"),
   
    )
  name=models.CharField(max_length=100)
  gender=models.CharField(max_length=10,choices=gender_choices)
  age=models.IntegerField()
  email=models.CharField(max_length=100)
  state=models.CharField(max_length=50,null=True, blank=True)
  address=models.TextField()
  contact_number=models.CharField(max_length=15)
  blood_group=models.CharField(max_length=30)
  last_donated_date=models.CharField(max_length=30)
  major_illness=models.CharField(max_length=200)
  
  b_request_id=models.ForeignKey(BRequests,null=True,on_delete=models.SET_NULL,blank=True)

  def __str__(self):
    return self.name

class Contact_Us(models.Model):
  firstname=models.CharField(max_length=100,)
  lastname=models.CharField(max_length=100,)
  email=models.CharField(max_length=100, null=True)
  subject=models.TextField()

  def __str__(self):
    return self.firstname



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
