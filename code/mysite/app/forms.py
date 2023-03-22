from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['collateral']

    def __init__(self, *args, **kwargs):
        super(Contract, self).__init__(*args, **kwargs)
        self.fields['collateral'].widget.attrs['accept'] = 'image/*,video/*'
        self.fields['collateral'].widget.attrs['multiple'] = 'multiple'
        self.fields['collateral'].widget.attrs['class'] = 'form-control'