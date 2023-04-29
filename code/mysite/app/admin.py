from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User, Contract, NFTContract, LoanRequest, Negotiation

admin.site.register(User, UserAdmin)
admin.site.register(Contract)
admin.site.register(NFTContract)
admin.site.register(LoanRequest)
admin.site.register(Negotiation)