from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import time, requests

from .models import WebPage

