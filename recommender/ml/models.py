from django.db import models
from django.contrib.auth.models import User

class Crop(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    season = models.CharField(max_length=80, blank=True)
    soil_type = models.CharField(max_length=120, blank=True)
    fertilizer_tips = models.TextField(blank=True)
    image = models.ImageField(upload_to="crops/", blank=True, null=True)

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    n = models.FloatField()
    p = models.FloatField()
    k = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    predicted_crop = models.CharField(max_length=80)
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.predicted_crop}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
