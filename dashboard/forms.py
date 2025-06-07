from django import forms

class TweetForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'What’s happening?'}),
        max_length=280,
        label=''
    )