from django.db import models
from django.utils.translation import *

# Create your models here.
class WebPage(models.Model):
    """ Model, which describes a response of the request to the specific web-page. """
    url = models.URLField(verbose_name=ugettext_lazy('Url'))
    http_code = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=ugettext_lazy('HTTP code'))
    ip_address = models.CharField(max_length=15, null=True, blank=True, verbose_name=ugettext_lazy('IP address'))
    timeout = models.FloatField(null=True, blank=True, verbose_name=ugettext_lazy('Timeout'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Updated at'))

    class Meta:
        verbose_name = ugettext_lazy('Web page')
        verbose_name_plural = ugettext_lazy('Web pages')
    
    def __str__(self):
        return self.url