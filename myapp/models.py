from django.db import models

# Create your models here.
class LoginTable(models.Model):
    username  = models.CharField(max_length=30,blank=True,null=True)
    password = models.CharField(max_length=30,blank=True,null=True)
    usertype = models.CharField(max_length=30,blank=True,null=True)
    status = models.CharField(max_length=100,blank=True,null=True)

class usertable(models.Model):
    Name = models.CharField(max_length=30,blank=True,null=True)
    phone_number = models.CharField(max_length=30,blank=True,null=True)
    loginid = models.ForeignKey(LoginTable,models.CASCADE,blank=True,null=True)
    emailid = models.CharField(max_length=100,blank=True,null=True)
    place = models.CharField(max_length=50,blank=True,null=True)
    img=models.FileField(blank=True,null=True)


class FileTable(models.Model):
    userid = models.ForeignKey(LoginTable,models.CASCADE,blank=True,null=True)
    file=models.FileField(blank=True,null=True)
    
from django.db import models

class SecureFile(models.Model):
    userid=models.ForeignKey(LoginTable,models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='secure_files/')
    encrypted_key = models.BinaryField()  # Store AES key encrypted with RSA
    created_at = models.DateTimeField(auto_now_add=True)
    aes_key=models.CharField(max_length=255,null=True,blank=True)  # Save AES key
    des3_key=models.CharField(max_length=255,null=True,blank=True)  # Save DES3 key
    blowfish_key=models.CharField(max_length=255,null=True,blank=True) 

    # def _str_(self):
    #     return self.title

class Rating(models.Model):
    userid=models.ForeignKey(LoginTable,models.CASCADE,blank=True,null=True)
    rating=models.IntegerField()
    feedback=models.CharField(max_length=100,null=True,blank=True)
    create_at=models.DateField(auto_now_add=True,null=True,blank=True)