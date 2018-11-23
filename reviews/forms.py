from django import forms
from .models import Reviews

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ('created_date', 'product')