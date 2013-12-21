from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import auth

from jsend import RSuccess, RFail, RError
import json
import urllib, urllib2


from .decorators import kuzines_api
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
@kuzines_api
def getListFromGoogleMap(request):
    # if request.method != 'POST':
    #     return FailResWithMsg("POST method expected")
    if request.DATA.has_key('latitude') and request.DATA.has_key('longitude'):
        latitude = request.DATA['latitude']
        longitude = request.DATA['longitude']
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
    resurl = urllib2.urlopen(reque)
    resfile = resurl.read()
    resjson = json.loads(resfile)

    if not resjson['status'] == "OK" and not resjson['status'] == "ZERO_RESULTS":
        return ErrorRes(resjson['status'])

    # names = [entry["name"] if "name" in entry else None for entry in jdata["results"]]
    entries = []
    for entry in resjson["results"]:
        tmp = {}
        if entry.has_key("name"):
            tmp["name"] = entry["name"]
        if entry.has_key("vicinity"):
            tmp["address"] = entry["vicinity"]
        if tmp:
            entries.append(tmp)
    return SuccessRes(entries)



from django.contrib.auth.models import User

@require_POST
@csrf_exempt
@kuzines_api
def sign_up(request):
    # assuem all inputs are valid. i.e. username is an email address
    if request.DATA.has_key('firstname') and request.DATA.has_key('username') and request.DATA.has_key('password'):
        firstname = request.DATA['firstname']
        username = request.DATA['username']
        password = request.DATA['password']
    else:
        return FailResWithMsg("paras not found")
    if request.DATA.has_key('lastname'):
        lastname = request.DATA['lastname']
    # birthday not done
    # location not done

    # newUser = Users(firstname = firstname, username = username, password = password)
    if User.objects.filter(username = username).exists():
        return FailResWithMsg("User already exists")
    newUser = User.objects.create_user(username = username, password = password)
    # username is the primary key, serve as email
    if newUser is None:
        return ErrorRes("Error registering new user")
    
    newUser.first_name = firstname
    if request.DATA.has_key('lastname'):
        newUser.last_name = lastname
    newUser.save()
    return SuccessRes("New user created")



@require_POST
@csrf_exempt
@kuzines_api
def log_in(request):
    if request.DATA.has_key('username'):
        username = request.DATA['username']
    else:
        return FailResWithMsg("username not found")
    if request.DATA.has_key('password'):
        password = request.DATA['password']
    else:
        return FailResWithMsg("password not found")

    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return SuccessRes("You are successfully logged in")
    else:
        return FailResWithMsg("username and password dismatch")


@csrf_exempt
@kuzines_api
def is_login(request):
    if request.user.is_authenticated():
        return SuccessRes("You are currently logged in")
    else:
        return FailResWithMsg("You are not logged in")


from django.contrib.auth.decorators import login_required
@login_required
@require_POST
@csrf_exempt
@kuzines_api
def log_out(request):
    auth_logout(request)
    return SuccessRes("You are successfully logged in")


from .models import Posts

@require_POST
@csrf_exempt
@kuzines_api
def newpost(request):
    """
    required paras:
    string username
    string content
    *location location
    """
    if request.DATA.has_key('username'):
        username = request.DATA['username']
    else:
        return FailResWithMsg("username not found")
    if request.DATA.has_key('content'):
        content = request.DATA['content']
    else:
        return FailResWithMsg("content not found")
    # location not done

    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return FailResWithMsg("User not exists")

    newPost = Posts(content = content, user = user)
    newPost.save()
    return SuccessRes("New feed posted on " + user)










def SuccessRes(data):
    res = RSuccess()
    res.data = data
    return HttpResponse(json.dumps(res), content_type = "application/json")

def FailResWithMsg(message):
    res = RFail()
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")

def ErrorRes(message):
    res = RError()
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")
