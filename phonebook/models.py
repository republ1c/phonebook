from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'user'
        ordering = ['user_name']

    user_name = models.CharField(max_length=200, default='Name')
    user_surname = models.CharField(max_length=200, blank=True)
    user_email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.user_name} {self.user_surname} {self.user_email}"
        # return self.user_name


class PhoneNumber(models.Model):
    class Meta:
        db_table = 'phonenumber'

    phonenumber_user = models.ForeignKey(User, on_delete=models.CASCADE)
    phonenumber_city = models.IntegerField(default=0)
    phonenumber_mobile = models.IntegerField(default=0)
    phonenumber_other = models.IntegerField(default=0)

    def __str__(self):
        return f"City: {self.phonenumber_city} Mobile: {self.phonenumber_mobile} Other: {self.phonenumber_other}"
