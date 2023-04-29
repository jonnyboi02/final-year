from django.db import models

from django.contrib.auth.models import AbstractUser

    # geth --http.api "personal,eth,net,web3" --miner.etherbase 0x90331b6e55da29a705c28c5dbe6d5b47e23c7aae --networkid 16969 --datadir "./data" --bootnodes enode://e297a68f525b4f12c63a783b69e9a15fb00db71070f037c14af1298f3464c2dce1659531b73416c57fab0138f45051bd01b452f3b9cdfeda7ebd157ae375cf1f@127.0.0.1:0?discport=30301 --port 30303 --ipcdisable --syncmode full --http --allow-insecure-unlock --http.corsdomain "*" --http.port 8547 --unlock 0x90331B6e55DA29A705C28C5DbE6d5B47E23C7aae --password password.txt --mine console  --unlock 0
class Negotiation(models.Model):
    # customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='negotiations')
    # bank = models.ForeignKey(User, on_delete=models.CASCADE, related_name='negotiation_offers')
    amount = models.TextField()
    password = models.TextField()
    user = models.TextField()
    customer_offer = models.BooleanField(default=False)
    bank_offer = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='negotiation_photos', blank=True)
    description = models.TextField(blank=True)
    accepted = models.BooleanField(default=False)
    conditions = models.FileField(upload_to='conditions', blank=True)



    def __str__(self):
        return f'Negotiation {self.pk}'

class LoanRequest(models.Model):
    lender = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    collateralValue = models.CharField(max_length=50)
    collateralHolder = models.CharField(max_length=50)
    collateralURL = models.CharField(max_length=250)
    loanApproved = models.BooleanField()
    loanWaiting = models.BooleanField()
    price = models.CharField(max_length=50)
    request_time = models.DateTimeField(auto_now_add=True)



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

