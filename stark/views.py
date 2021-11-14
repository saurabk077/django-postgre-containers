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

url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=CNY&apikey=APIKEY'


# r = requests.get(url)
# data = r.json()
#
# # {'Realtime Currency Exchange Rate': {'1. From_Currency Code': 'BTC', '2. From_Currency Name': 'Bitcoin', '3. To_Currency Code': 'USD', '4. To_Currency Name': 'United States Dollar', '5. Exchange Rate': '63892.61000000',
# # '6. Last Refreshed': '2021-11-13 08:50:01', '7. Time Zone': 'UTC', '8. Bid Price': '63892.60000000', '9. Ask Price': '63892.61000000'}}
#
#
# exchange_data = ExchangeRate.objects.create(from_currency_code=data['Realtime Currency Exchange Rate']['1. From_Currency Code'],
#                                             from_currency_name=data['Realtime Currency Exchange Rate']['2. From_Currency Name'],
#                                             to_currency_code=data['Realtime Currency Exchange Rate']['3. To_Currency Code'],
#                                             to_currency_name=data['Realtime Currency Exchange Rate']['4. To_Currency Name'],
#                                             exchange_rate=data['Realtime Currency Exchange Rate']['5. Exchange Rate'],
#                                             last_refreshed=data['Realtime Currency Exchange Rate']['6. Last Refreshed'],
#                                             time_zone=data['Realtime Currency Exchange Rate']['7. Time Zone'],
#                                             bid_price=data['Realtime Currency Exchange Rate']['8. Bid Price']
#                                             )

# def home(request):
#     template_name = "home.html"
#     # # template = loader.get_template("home.html")
#     # name = request.POST['u_name']  # u_name is the name of the input tag
#     # age = request.POST['age']
#     # address = request.POST['address']
#     # print('name', address)
#
#     return render(request, "stark/home.html", {})
#
#
def get_exchange_rate(request):
    try:
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
    except data.DoesNotExist:
        raise Http404("Data does not exist")

    # def check(request):
    #     name = request.POST['u_name']  # u_name is the name of the input tag
    #     age = request.POST['age']
    #     address = request.POST['address']
    #     print('name', name)
    #
    #     # return HttpResponse('<h1>Page was found {exchange_data}</h1>')
    # return HttpResponse(json.dumps(data), content_type='application/json')
class HomeView(TemplateView):
    template_name = 'stark/home.html'
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=CNY&apikey=APIKEY'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            FROM_CURRENCY = form.cleaned_data['from_currency']
            TO_CURRENCY = form.cleaned_data['to_currency']
            print(FROM_CURRENCY,TO_CURRENCY)
            url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=APIKEY'.format(FROM_CURRENCY,TO_CURRENCY)
            print(url)
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

        return HttpResponse(json.dumps(data), content_type='application/json')

