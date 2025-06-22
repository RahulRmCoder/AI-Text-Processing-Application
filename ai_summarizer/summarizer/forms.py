from django import forms

class SummarizerForm(forms.Form):
    input_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        label="Enter text to process"
    )
    
    OPERATION_CHOICES = [
        ('summarize', 'Summarize'),
        ('rewrite', 'Rewrite'),
    ]
    
    operation = forms.ChoiceField(
        choices=OPERATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Choose operation"
    )
    
    # Match the style choices from the serializer
    STYLE_CHOICES = [
        ('formal', 'Formal'),
        ('casual', 'Casual'),
        ('creative', 'Creative'),
        ('academic', 'Academic'),
        ('business', 'Business')

    ]
    
    style = forms.ChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Rewrite style",
        required=False,
    )
