from django import forms

class PreferenceForm(forms.Form):
    EXAM_CHOICES = [('Advanced', 'Advanced'), ('Mains', 'Mains')]
    SEAT_CHOICES = [('OPEN', 'OPEN'), ('SC', 'SC'), ('ST', 'ST'), ('OBC-NCL', 'OBC-NCL'), ('OPEN (PwD)', 'OPEN (PwD)'), ('EWS', 'EWS')]
    QUOTA_CHOICES = [('AI', 'AI'), ('HS', 'HS'), ('OS', 'OS')]
    GENDER_CHOICES = [('Neutral', 'Neutral'), ('Female', 'Female')]

    exam = forms.ChoiceField(choices=EXAM_CHOICES)
    seat_type = forms.ChoiceField(choices=SEAT_CHOICES)
    rank = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'font-size: 1.2em; border: 1px solid #ccc; border-radius: 5px; width: 30%; position: absolute; left: 43vw'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    quota = forms.ChoiceField(choices=QUOTA_CHOICES, required=False)