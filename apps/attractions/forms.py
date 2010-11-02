from django import forms

class TagSearch(forms.Form):
    tag_search = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class':'location'}),)
