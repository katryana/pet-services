# Generated by Django 4.2.5 on 2023-10-16 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("training_centers", "0003_alter_dog_age_alter_specialist_years_of_experience"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dog",
            name="breed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dogs",
                to="training_centers.breed",
            ),
        ),
    ]
