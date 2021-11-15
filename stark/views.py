from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from .models import ExchangeRate
from .forms import HomeForm
import os

import requests
import json

APIKEY = os.environ.get('APIKEY')

class HomeView(TemplateView):
    template_name = 'stark/home.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = HomeForm(request.POST)
        if form.is_valid():
            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']
            url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=APIKEY'.format(from_currency,to_currency)
            r = requests.get(url)
            data = r.json()

            exchange_data = ExchangeRate.objects.create(
                from_currency_code=data['Realtime Currency Exchange Rate']['1. From_Currency Code'],
                from_currency_name=data['Realtime Currency Exchange Rate']['2. From_Currency Name'],
                to_currency_code=data['Realtime Currency Exchange Rate']['3. To_Currency Code'],
                to_currency_name=data['Realtime Currency Exchange Rate']['4. To_Currency Name'],
                exchange_rate=data['Realtime Currency Exchange Rate']['5. Exchange Rate'],
                last_refreshed=data['Realtime Currency Exchange Rate']['6. Last Refreshed'],
                time_zone=data['Realtime Currency Exchange Rate']['7. Time Zone'],
                bid_price=data['Realtime Currency Exchange Rate']['8. Bid Price']
            )

        #return HttpResponse(json.dumps(data), content_type='application/json')
        return JsonResponse(data, json_dumps_params={'indent': 2})

