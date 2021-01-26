from django import forms

class CreateArticleForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

