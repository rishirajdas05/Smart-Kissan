# Generated for CropReco Pro
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Crop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(max_length=120, unique=True)),
                ("description", models.TextField(blank=True)),
                ("season", models.CharField(blank=True, max_length=80)),
                ("soil_type", models.CharField(blank=True, max_length=120)),
                ("fertilizer_tips", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="crops/")),
            ],
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="auth.user")),
            ],
        ),
        migrations.CreateModel(
            name="Recommendation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mode", models.CharField(choices=[("manual", "Manual"), ("auto", "Auto")], default="manual", max_length=10)),
                ("n", models.FloatField()),
                ("p", models.FloatField()),
                ("k", models.FloatField()),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("ph", models.FloatField()),
                ("rainfall", models.FloatField()),
                ("location", models.CharField(blank=True, default="", max_length=140)),
                ("predicted_crop", models.CharField(max_length=80)),
                ("confidence", models.FloatField(default=0.0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="recommendations", to="auth.user")),
            ],
        ),
        migrations.CreateModel(
            name="CropPriceRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("crop", models.CharField(max_length=80)),
                ("market", models.CharField(blank=True, default="", max_length=80)),
                ("year", models.PositiveIntegerField()),
                ("month", models.PositiveIntegerField()),
                ("price_inr_per_quintal", models.FloatField()),
            ],
            options={
                "indexes": [models.Index(fields=["crop", "year", "month"], name="recommender_crop_year_month_idx")],
            },
        ),
        migrations.CreateModel(
            name="PricePrediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("crop", models.CharField(max_length=80)),
                ("market", models.CharField(blank=True, default="", max_length=80)),
                ("year", models.PositiveIntegerField()),
                ("month", models.PositiveIntegerField()),
                ("predicted_price_inr_per_quintal", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="price_predictions", to="auth.user")),
            ],
        ),
    ]
