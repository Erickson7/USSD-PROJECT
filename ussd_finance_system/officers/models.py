from django.db import models



class Officer(models.Model):

    full_name = models.CharField(
        max_length=100
    )

    username = models.CharField(
        max_length=50,
        unique=True
    )

    password = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.full_name