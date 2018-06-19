'''
Created on 14.06.2018

@author: makki
'''
from django import forms

class TimePlotForm(forms.Form):
    start_time=forms.DateTimeField()
    end_time=forms.DateTimeField()
    location1 = forms.CharField(max_length=30)
    location2 = forms.CharField(max_length=30)
    
    def submit_button_clicked(self):
        print("submit_button_clicked(self) CALLED")