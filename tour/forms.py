# tour/forms.py
from django import forms

class ServiceMetricsForm(forms.Form):
    avg_arrival_rate = forms.IntegerField(label='Среднее число поступающих заявок в сутки', min_value=1)
    avg_service_time_minutes = forms.FloatField(label='Средняя длительность переговоров в минутах', min_value=0.1)
    num_channels = forms.IntegerField(label='Количество телефонных аппаратов', min_value=1)
