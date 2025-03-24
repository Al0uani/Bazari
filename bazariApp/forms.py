from django import forms
from .models import user,product

class SignUpFrom(forms.ModelForm):
    class Meta():
        model = user
        fields = ['Username', 'Firstname', 'Lastname', 'Birth', 'Email', 'Password','Pfp']
        widgets = {
            'Birth': forms.DateInput(attrs={'type': 'date'}),
        }

    # You can also handle the Pfp field here explicitly if needed
    Pfp = forms.ImageField(required=False)

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['Name', 'Description','Price','Picture_main','Picture_second', 'Picture_third', 'category']

    
