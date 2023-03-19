from django import forms
from .models import NFT

class NFTForm(forms.ModelForm):
    class Meta:
        model = NFT
        fields = ['collateral']

    def __init__(self, *args, **kwargs):
        super(NFTForm, self).__init__(*args, **kwargs)
        self.fields['collateral'].widget.attrs['accept'] = 'image/*,video/*'
        self.fields['collateral'].widget.attrs['multiple'] = 'multiple'
        self.fields['collateral'].widget.attrs['class'] = 'form-control'