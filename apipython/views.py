"""
Views
"""
from datetime import datetime

from django.http import JsonResponse
from pandas.tseries.offsets import BDay

from apipython.api.api import CoinsAPI


def define_date_request():
    """
    Gera um array de forma automatica
    com as datas dos ultimos 5 dias uteis
    """
    today_now = datetime.today()
    array_dates_ultils = []
    for i in range(6):
        str_formarting = today_now - BDay(i)
        str_formarting = str_formarting.strftime("%Y-%m-%d")
        array_dates_ultils.append(str_formarting)
    array_dates_ultils.remove(array_dates_ultils[0])

    return array_dates_ultils


def request_data_comply(request):
    """
    Requisita os dados da API
    """
    bases = ["USD", "EUR", "JPY", "BRL"]
    dates_array = define_date_request()
    coins_api = CoinsAPI
    actual_value_coins = {}
    for base in bases:
        array_return_values = {}
        for date in dates_array:
            response_vatcomply_api = coins_api.request_uri(date, base)
            date_request_return = response_vatcomply_api.get("date")
            filter_response = filter_array(response_vatcomply_api, bases)
            array_return_values[date_request_return] = filter_response
        actual_value_coins[base] = array_return_values
    payload_data = lapid_array(actual_value_coins, bases, dates_array)

    return JsonResponse(payload_data, safe=False)


def filter_array(data_json, coins):
    """
    Filtra o objeto retornado da API
    """
    rates = data_json.get("rates")
    # Filtra o objeto retornado
    series_list_values = []
    for coin in coins:
        series_list_values.append(rates.get(coin))
    # Arredonda os valores filtrados do array
    payload_array = []
    for i in series_list_values:
        round_number = round(i, 3)
        payload_array.append(round_number)

    return payload_array


def lapid_array(actual_value_coins, bases, dates_array):
    """
    Lapida os dados baseado no JSON criado
    """
    payload = {}
    for base in bases:
        base_vetor = actual_value_coins.get(base)
        array_values_coins_usd = []
        array_values_coins_eur = []
        array_values_coins_jpy = []
        array_values_coins_brl = []
        list_coins_values = {}
        for date in dates_array:
            position_dict = base_vetor.get(date)
            if base == "USD":
                position_dict.remove(position_dict[0])
                array_values_coins_eur.append(position_dict[0])
                array_values_coins_jpy.append(position_dict[1])
                array_values_coins_brl.append(position_dict[2])
            if base == "EUR":
                position_dict.remove(position_dict[1])
                array_values_coins_usd.append(position_dict[0])
                array_values_coins_jpy.append(position_dict[1])
                array_values_coins_brl.append(position_dict[2])
            if base == "JPY":
                position_dict.remove(position_dict[2])
                array_values_coins_usd.append(position_dict[0])
                array_values_coins_eur.append(position_dict[1])
                array_values_coins_brl.append(position_dict[2])
            if base == "BRL":
                position_dict.remove(position_dict[3])
                array_values_coins_usd.append(position_dict[0])
                array_values_coins_eur.append(position_dict[1])
                array_values_coins_jpy.append(position_dict[2])
        if base == "USD":
            list_coins_values["EUR"] = array_values_coins_eur
            list_coins_values["JPY"] = array_values_coins_jpy
            list_coins_values["BRL"] = array_values_coins_brl
        if base == "EUR":
            list_coins_values["USD"] = array_values_coins_usd
            list_coins_values["JPY"] = array_values_coins_jpy
            list_coins_values["BRL"] = array_values_coins_brl
        if base == "JPY":
            list_coins_values["USD"] = array_values_coins_usd
            list_coins_values["EUR"] = array_values_coins_eur
            list_coins_values["BRL"] = array_values_coins_brl
        if base == "BRL":
            list_coins_values["USD"] = array_values_coins_usd
            list_coins_values["EUR"] = array_values_coins_eur
            list_coins_values["JPY"] = array_values_coins_jpy
        payload[base] = list_coins_values
        
    payload["series_date"] = formating_date(dates_array)

    return payload

def formating_date(dates_array):
    """
    Formata a data para o padrão Brasil
    """
    format_date = []
    for i in dates_array:
        original_date = datetime.strptime(i, '%Y-%m-%d')
        formatted_date = original_date.strftime("%d/%m/%Y")
        format_date.append(formatted_date)
        
    return format_date