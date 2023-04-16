from django.db import models

from django.contrib.auth.models import AbstractUser

class LoanRequest(models.Model):
    amount = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    collateralValue = models.CharField(max_length=50)
    collateralHolder = models.CharField(max_length=50)
    collateralURL = models.CharField(max_length=250)
    loanApproved = models.BooleanField()



class NFTContract(models.Model):
    address = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.address
    
# Create your models here.
class User(AbstractUser):
    key_store = models.FileField(blank=True, null=True)
    public_key = models.CharField(max_length=250)

    username = models.CharField(unique=True, max_length=150)


    def get_public_key(self):
        return self.public_key
    
    def set_public_key(self, key):
        self.public_key = key

    def get_username(self):
        return self.username

class Contract(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract_address = models.TextField(max_length=255)
    collateral = models.FileField(upload_to='collateral') 
    

    def get_collateral_url(self):
        return self.collateral.url
    
    def get_address(self):
        return self.contract_address

