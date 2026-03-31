from django import forms

def _w(placeholder, input_type="text"):
    return forms.TextInput(attrs={"class": "sk-input", "placeholder": placeholder, "type": input_type})

def _wn(placeholder):
    return forms.NumberInput(attrs={"class": "sk-input", "placeholder": placeholder})

class ManualRecommendationForm(forms.Form):
    nitrogen = forms.FloatField(label="Nitrogen (N)", widget=_wn("e.g., 60"))
    phosphorus = forms.FloatField(label="Phosphorus (P)", widget=_wn("e.g., 40"))
    potassium = forms.FloatField(label="Potassium (K)", widget=_wn("e.g., 40"))
    temperature = forms.FloatField(label="Temperature (°C)", widget=_wn("e.g., 25"))
    humidity = forms.FloatField(label="Humidity (%)", widget=_wn("e.g., 55"))
    ph = forms.FloatField(label="Soil pH", widget=_wn("e.g., 6.8"))
    rainfall = forms.FloatField(label="Rainfall (mm)", widget=_wn("e.g., 120"))

class AutoCityForm(forms.Form):
    cities = forms.CharField(label="Cities (comma separated)", widget=_w("e.g., Delhi, Jaipur, Bhopal, Gwalior"))
    ph = forms.FloatField(label="Optional Soil pH", required=False, widget=_wn("e.g., 6.8 (leave blank to auto)"))

class PriceForm(forms.Form):
    crop = forms.CharField(label="Crop", widget=_w("e.g., wheat, rice, cotton"))
    mandi = forms.CharField(label="Market / Mandi", widget=_w("e.g., Gwalior Mandi / Azadpur Delhi"))

class SoilForm(forms.Form):
    ph = forms.FloatField(label="Soil pH", widget=_wn("e.g., 6.8"))
    moisture = forms.FloatField(label="Moisture (%)", widget=_wn("e.g., 45"))

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Name", widget=_w("Your name"))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"class": "sk-input sk-textarea", "placeholder": "Write your feedback..."}))
