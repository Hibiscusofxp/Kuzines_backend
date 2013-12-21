# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.conf import settings



def index(request):
	return HttpResponse("Hi")


from jsend import RSuccess, RFail, RError
from django.contrib import auth
import json
import urllib, urllib2

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getListFromGoogleMap(request):
    if request.method != 'POST':
        return FailResWithMsg("POST method expected")
    if request.POST.has_key('latitude') and request.POST.has_key('longitude'):
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
    else:
        return FailResWithMsg("latitude or longitude not found")

    plain_paras = {
        'location': latitude + ',' + longitude,
        # 'location': map(float, [latitude, longitude]).joins(','),
        # 'location': "%d,%d" % (latitude, longitude),
        'types': 'food',
        'radius': 500,
        'sensor': 'false',
        'key': settings.MY_GOOGLE_API_KEY,
    }
    paras = urllib.urlencode(plain_paras)
    reque = urllib2.Request('https://maps.googleapis.com/maps/api/place/nearbysearch/json?' + paras)
    res = urllib2.urlopen(reque)
    r = res.read()
    response = json.loads(r)

    # names = [entry["name"] if "name" in entry else None for entry in jdata["results"]]
    names = []
    for entry in response["results"]:
        if entry.has_key("name"):
            names.append(entry["name"])
    jdata = {}
    jdata["results"] = names
    jdata["status"] = response["status"]
    return HttpResponse(json.dumps(jdata), content_type = "application/json")


from jsend import RSuccess, RFail, RError

def FailResWithMsg(message):
    res = RFail()
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")