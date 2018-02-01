# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

import json, datetime, re
from decimal import Decimal as D
from collections import OrderedDict

pat_date = re.compile('\d{4}-\d{2}-\d{2}')

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, str) and re.search("\d{4}-\d{2}-\d{2}", obj):
            try:
                rez = datetime.datetime.strptime(obj, "%Y-%m-%d")
            except:
                pass
                raise
            else:
                print(rez)
                return rez
        return json.JSONEncoder.default(self, obj)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, D):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def date_parser(in_str):
    in_str = in_str.replace('"', '')
    if isinstance(in_str, str) and re.search("\d{4}-\d{2}-\d{2}", in_str):
        try:
            rez = datetime.datetime.strptime(in_str, "%Y-%m-%d").date()
        except:
            pass
            raise
        else:
            print(rez)
            return rez

def check_date_str(in_fromdate, in_todate):
    """Check input string represented date
    for format '2000-01-01' """
    if not pat_date.match(in_fromdate) or not pat_date.match(in_todate):
        return {'state': 422, "mesg": "Wrong date format"}
    else:
        return  {'state': 400, "mesg":''}

def check_date(in_fromdate, in_todate):
    """Check input date
        for from date must be < to date"""
    if in_fromdate > in_todate:
        return {'state': 422, "mesg": "From_date must be less then to_date"}
    else:
        return {'state': 400, "mesg": ''}

# Create your views here.

def index(request):
    return render_to_response('revenue/index.html')

def getSales(request):
    from revenue.models import Revenue
    # import pdb; pdb.set_trace()
    # TODO realize by loads
    # TODO differ response by state
    date_from_str = json.dumps(request.GET.get('from'))
    date_to_str = json.dumps(request.GET.get('to'))

    state = check_date_str(date_from_str, date_to_str)

    date_from = date_parser(date_from_str)
    date_to = date_parser(date_to_str)

    state = check_date(date_from, date_to)

    rez = OrderedDict()
    rev_total = 0

    rez['from'] = date_from.isoformat()
    rez['to'] = date_to.isoformat()
    rez['goods'] = []

    for obj in Revenue.objects.filter(date_sold__range=[date_from, date_to]):
        rez['goods'].append({'title': obj.good, 'revenue': obj.revenue})
        rev_total += obj.revenue
    rez['total_revenue'] = rev_total

    if rez:
        return HttpResponse(json.dumps(rez, cls=DecimalEncoder), content_type='application/json')
    else:
        assert False
