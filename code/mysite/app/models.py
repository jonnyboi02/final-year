from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    private_key = models.CharField(max_length=250)
    key_store = models.FileField(blank=True, null=True)
    public_key = models.CharField(max_length=250)

    def get_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key


class NFT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract_address = models.TextField(max_length=255)
    collateral = models.FileField(upload_to='collateral') 

    def get_collateral_url(self):
        return self.collateral.url
    
    def get_address(self):
        return self.contract_address

