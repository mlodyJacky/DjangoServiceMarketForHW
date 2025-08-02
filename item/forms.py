from django import forms
from django.core.exceptions import ValidationError
from .models import Item
from core.validators import (
    validate_no_bad_words,
    validate_image_is_safe,
    validate_image_is_hotwheels

)

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        validators=[validate_no_bad_words],
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES})
    )
    
    description = forms.CharField(
        max_length=2000,
        required=False,
        validators=[validate_no_bad_words],
        widget=forms.Textarea(attrs={'class': INPUT_CLASSES})
    )
    image = forms.ImageField(
        required=True,
        validators=[validate_image_is_safe, validate_image_is_hotwheels],
        widget=forms.FileInput(attrs={'class': INPUT_CLASSES})
    )

    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price > 100000:
            raise ValidationError("Cena jest za duża")
        return price


class EditItemForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        validators=[validate_no_bad_words],
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES})
    )
    
    description = forms.CharField(
        max_length=2000,
        required=False,
        validators=[validate_no_bad_words],
        widget=forms.Textarea(attrs={'class': INPUT_CLASSES})
    )
    image = forms.ImageField(
        required=True,
        validators=[validate_image_is_safe, validate_image_is_hotwheels],
        widget=forms.FileInput(attrs={'class': INPUT_CLASSES})
    )

    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image')
        widgets = {
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price > 100000:
            raise ValidationError("Cena jest za duża.")
        return price
