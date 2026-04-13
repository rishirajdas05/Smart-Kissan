from django.db import models
from django.contrib.auth.models import User


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    page = models.CharField(max_length=100)
    action = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-timestamp']


class CropRecommendation(models.Model):
    METHOD_CHOICES = [('manual','Manual'),('auto','Auto')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    crop_name = models.CharField(max_length=100)
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    rainfall = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    # Feedback
    feedback = models.CharField(max_length=10, blank=True)  # 'helpful' or 'not_helpful'
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-timestamp']


class SoilAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_analyses')
    ph = models.FloatField()
    moisture = models.FloatField()
    tips = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-timestamp']


class SupportQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    farm_size = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    language = models.CharField(max_length=5, default='en', choices=[('en','English'),('hi','Hindi')])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username}'s profile"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    role = models.CharField(max_length=20)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['timestamp']


class YieldEstimate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yield_estimates')
    crop = models.CharField(max_length=100)
    land_area = models.FloatField()
    area_unit = models.CharField(max_length=10, default='acres')
    estimated_yield = models.FloatField()
    estimated_income = models.FloatField()
    msp_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)