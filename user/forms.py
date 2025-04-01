from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Napisz coś o sobie... (maks. 300 znaków)',
                'maxlength': '300'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-500 file:mr-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            })
        }