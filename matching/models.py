from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    major = models.CharField(max_length=100, blank=True)
    grad_year = models.CharField(max_length=4)
    bio = models.TextField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    #     team = models.ManyToManyField('Team', blank=True)
    matches = models.ManyToManyField('Profile', blank=True)
    profilePicture = models.ImageField(upload_to='images', blank=True)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Profile.objects.get(pk=self.pk)
            if this.picture != self.picture:
                this.picture.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

