from .validators import file_size

from django.db import models
# Create your models here.
class Video(models.Model):
    Subject_name = [
        ('english', 'ENGLISH'),
        ('maths', 'MATHS'),
        ('malayalam', 'MALAYALAM'),
        ('dance', 'DANCE'),
        ('art', 'Art & Craft'),
    ]
    Class_name = [
        ('prekg', 'PreKg'),
        ('lkg', 'LKG'),
        ('ukg', 'UKG'),
    ]
    classname = models.CharField(max_length=100,choices=Class_name,default='prekg')
    subjname = models.CharField(max_length=50,choices=Subject_name,default='english')
    title = models.CharField(max_length=100,null=True)
    video = models.FileField(upload_to="video/%y", validators=[file_size],null=True)

    def __str__(self):
        return self.title
