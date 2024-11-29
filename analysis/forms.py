from django import forms
from .models import BloodAnalysis

class BloodAnalysisForm(forms.ModelForm):
    class Meta:
        model = BloodAnalysis
        fields = ['image']
