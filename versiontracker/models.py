from django.db import models


class AppEnvironment(models.Model):
    #Exp: dev, test, stage, prod
    env_name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.env_name

class AppName(models.Model):
    app_name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.app_name

class AppVersion(models.Model):
    name = models.ForeignKey(AppName, on_delete=models.CASCADE)
    environment = models.ForeignKey(AppEnvironment, on_delete=models.CASCADE)
    version = models.CharField(max_length=200)
    #exp 2021-05-01 14:00:00
    deploy_date = models.DateTimeField('date deployed', auto_now_add=True)
