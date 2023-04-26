from django.db import models
from django.urls import reverse
from polls.models import CustomUser,principal

my_choices=(
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class principalabout(models.Model):
    id=models.AutoField(primary_key=True)
    principal = models.ForeignKey(principal, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    profile_photo = models.ImageField(null=True,blank=True,upload_to='principalUpload')
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    cname = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=my_choices,blank=True, null=True)
    dob = models.DateField(max_length=8)
    qualification=models.CharField(max_length=10)
    from1 = models.DateField(max_length=8)
    to= models.DateField(max_length=8)
    join = models.DateField(max_length=8)
    seperate = models.DateField(max_length=8)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("hod:manage_principal",kwargs={"principal_id": self.id})

    def get_ingredients_children(self):
        return principalabout.objects.all()

    @property
    def photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

    def get_edit_url(self):
        return reverse("hod:edit_principal", kwargs={"principal_id": self.id})

    def get_delete_url(self):
        return reverse("hod:deleteform", kwargs={"pk": self.id})

class Principalabouts(models.Model):
    principal = models.ForeignKey(principalabout, on_delete=models.CASCADE, related_name='principalabouts',blank=False,null=False)
    cname = models.CharField(max_length=100)
    qualification=models.CharField(max_length=10)
    from1 = models.DateField(max_length=8)
    to= models.DateField(max_length=8)
    id = models.AutoField(primary_key=True)

class Schoolabout(models.Model):
    id=models.AutoField(primary_key=True)
    principal = models.ForeignKey(principal, blank=True, null=True, on_delete=models.SET_NULL,related_name='schoolss')
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("hod:manage_principal",kwargs={"principal_id": self.id})

    def get_edit_url(self):
        return reverse("hod:edit_about")
    
    def get_delete_url(self):
        return reverse("hod:delete_about")
