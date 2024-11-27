from django import forms

class ParameterForm(forms.Form):
    # Define your fields here
    field1 = forms.FloatField(label='Field 1')
    field2 = forms.FloatField(label='Field 2')
    # Add more fields as needed

class HospitalParameterForm(forms.Form):
    mdvp_fo = forms.FloatField(label='MDVP:Fo(Hz)')
    mdvp_fhi = forms.FloatField(label='MDVP:Fhi(Hz)')
    mdvp_flo = forms.FloatField(label='MDVP:Flo(Hz)')
    jitter_percent = forms.FloatField(label='Jitter(%)')
    jitter_abs = forms.FloatField(label='Jitter(Abs)')
    shimmer = forms.FloatField(label='Shimmer')
    shimmer_db = forms.FloatField(label='Shimmer(dB)')
    # Add more fields as needed
