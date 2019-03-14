from django import forms
from blog.models import Survey
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from lxml import html
import requests
from datetime import datetime
from django.forms.widgets import HiddenInput

class SurveyForm(forms.ModelForm):    
    surveyName = forms.CharField(label='Survey Name')
    location = forms.CharField(label='Beach')
    region = forms.CharField()
    dateSampled = forms.DateField(label='Date Sampled')
    transNumber = forms.IntegerField(label='Transect Number')
    startLat = forms.FloatField(label='Start Latitude')
    startLong = forms.FloatField(label='Start Longitude')
    endLat = forms.FloatField(label='End Latitude')
    endLong = forms.FloatField(label='End Longitude')
    clams = forms.TextInput()
    waterTemp = forms.CharField(label = "Sea Temperature")
    airTemp = forms.CharField(label = "Temperature")
    
    class Meta:
        model = Survey
        fields = {'surveyName', 'location', 'region', 'dateSampled', 'transNumber', 'startLat',
                  'startLong', 'endLat', 'endLong', 'clams', 'waterTemp', 'airTemp'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'surveyName',
            Row(
                Column('location', css_class='form-group col-md-6 mb-0'),
                Column('region', css_class='form-group col-md-6 mb-0'),
                Column('dateSampled', css_class='form-group col-md-6 mb-0'),
                Column('transNumber', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('startLat', css_class='form-group col-md-6 mb-0'),
                Column('startLong', css_class='form-group col-md-6 mb-0'),
                Column('endLat', css_class='form-group col-md-6 mb-0'),
                Column('endLong', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('waterTemp', css_class='form-group col-md-6 mb-0'),
                Column('airTemp', css_class='form-group col-md-6 mb-0'),
            ),
            'clams',
            self.helper.add_input(Submit('submit', 'Submit', css_class='submitButton'))
        )