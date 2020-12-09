from django.shortcuts import render
from django.utils.translation import *

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

import xlrd
import time
import requests
import logging

from .models import WebPage
from .serializers import WebPageSerializer
from .filters import WebPageFilter

logger = logging.getLogger(__name__)
# Create your views here.
class WebPageViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Lists all objects of :model:`main.WebPage`."""
    serializer_class = WebPageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WebPageFilter

    def get_queryset(self):
        logger.info(f"WebPages have been listed.")
        return WebPage.objects.all()


    @action(methods=['GET'], detail=False)
    def add(self, request):
        """This action creates new and unique objects of :model:`main.WebPage`."""
        
        file_path = ('../urls.xlsx')

        file = xlrd.open_workbook(file_path) # Opens excel file using xlrd lib.
        sheet = file.sheet_by_index(0) # First page of excel file.

        for i in range(1, sheet.nrows): # Begins from the second row, because the first row is a definition of the column.
            WebPage.objects.get_or_create(url=sheet.cell_value(i, 0)) # Creates objects from the first column.
            logger.info(f"WebPage with url {sheet.cell_value(i, 0)} has been created.")

        return Response({ugettext('message'): ugettext('finished')})
    
    @action(methods=['GET'], detail=False)
    def run(self, request):
        """This action sends requests through all web pages and saves response info"""
        
        web_pages = WebPage.objects.all() # Gets all urls.  
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"} # We need headers, because not all web-sites support python's requests.

        for web_page in web_pages: # Loop for sending requests to each web page.
            try:
                start = time.time() # Time when request was sent.
                response = requests.get('http://' + web_page.url,
                    headers=headers, 
                    stream=True, # Was used to get raw response and also allows iter_tools().
                    timeout=10 # Duration of the request in seconds.
                )
                end = time.time() # Time when response was accepted.
                
                web_page.timeout = end - start # Duration of the request.
                web_page.http_code = response.status_code # HTTTP status code.
                web_page.ip_address = response.raw._connection.sock.getpeername()[0] # IP address.
                web_page.save()
                logger.info(f"WebPage with url {web_page.url} has been succesfully proccessed.")

            except requests.exceptions.ConnectTimeout:
                end = time.time() # Time when exception occured.
                web_page.timeout = end - start # Duration.
                web_page.http_code = 408 # HTTP code - connection timed out.
                web_page.save()
                logger.info(f"WebPage with url {web_page.url} has been proccessed, with timed out connection.")

            except Exception as e:
                end = time.time() # Time when exception occured.
                web_page.timeout = end - start # Duration.
                web_page.http_code = 503 # HTTP code - service unavailable.
                web_page.save()
                logger.info(f"WebPage with url {web_page.url} has been proccessed, with unavailable service.")

        logger.info(f"{self.request.user} created comment: {serializer.data.get('message')}")
        return Response({ugettext('message'): ugettext('finished')})