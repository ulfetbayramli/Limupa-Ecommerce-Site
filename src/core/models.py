from django.db import models

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.subject} from {self.email}"

    class Meta:
        verbose_name = "Message from user"
        verbose_name_plural = "Messages from user"
