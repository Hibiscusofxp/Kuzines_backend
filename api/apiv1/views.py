from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.contrib import auth

from jsend import RSuccess, RFail, RError
import json
import urllib, urllib2


from .decorators import kuzines_api
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required





@require_POST
# @login_required
@csrf_exempt
@kuzines_api
def getListFromGoogleMap(request):
    # todo: the result of photo field is using "&amp;" as seperator. need to change to "&"?
    """ required_paras
    float latitude
    float longitude
    CAUTION: does not work if latitude and longitude are strings
        output_json
    string name
    string address
    string icon
    """
    # if request.method != 'POST':
    #     return FailResWithMsg("POST method expected")
    if request.DATA.has_key('latitude') and request.DATA.has_key('longitude'):
        latitude = float(request.DATA['latitude'])
        longitude = float(request.DATA['longitude'])
    else:
        return FailResWithMsg("latitude or longitude not found")

    plain_paras = {
        # 'location': latitude + ',' + longitude,
        # 'location': map(float, [latitude, longitude]).joins(','),
        'location': "%f,%f" % (latitude, longitude),
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
        # if entry.has_key("icon"):
        #     tmp["icon"] = entry["icon"]
        if entry.has_key("photos"):
            photo_paras = {
                'photoreference': entry["photos"][0]["photo_reference"],
                'maxwidth': 400,
                'sensor': 'false',
                'key': settings.MY_GOOGLE_API_KEY,
            }
            paras = urllib.urlencode(photo_paras)
            tmp["photo"] = 'https://maps.googleapis.com/maps/api/place/photo?' + paras
            # tmp["photo"].replace(r'&amp;', r'&')
            # one alternative is to use javascripte and show it directly
        if tmp:
            entries.append(tmp)
    return SuccessRes(data = entries)



from django.contrib.auth.models import User
from .models import MyUserInfo

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
    newUserMy = MyUserInfo(user = newUser)
    # username is the primary key, serve as email
    if newUser is None:
        return ErrorRes("Error registering new user")
    newUser.myuserinfo = newUserMy
    newUser.first_name = firstname
    if request.DATA.has_key('lastname'):
        newUser.last_name = lastname
    newUser.save()
    newUserMy.save()
    return SuccessRes(message = "New user created")



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
        return SuccessRes(message = "You are successfully logged in")
    else:
        return FailResWithMsg("username and password dismatch")


@csrf_exempt
@kuzines_api
def is_login(request):
    if request.user.is_authenticated():
        data = {
            'username': request.user.username,
        }
        return SuccessRes(data = data, message = "You are currently logged in")
    else:
        return FailResWithMsg("You are not logged in")


@require_POST
@login_required
@csrf_exempt
@kuzines_api
def log_out(request):
    auth.logout(request)
    return SuccessRes(message = "You have logged out")




from .models import Posts
import datetime

@require_POST
@login_required
@csrf_exempt
@kuzines_api
def newpost(request):
    """
    required paras:
    string username
    string content
    *location location
    """
    # one problem remain: what content includes quotation marks
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
    newPost.time = datetime.datetime.utcnow()
    newPost.save()
    return SuccessRes(message = "New feed posted on " + username)




@require_POST
@login_required
@csrf_exempt
@kuzines_api
def getPosts(request):
    """
    required paras:
    string username
    """
    # one problem remain: what if content includes quotation marks
    # location not done
    if request.DATA.has_key('username'):
        username = request.DATA['username']
    else:
        return FailResWithMsg("username not found")

    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return FailResWithMsg("User not exists")

    allposts = user.posts_set.all()
    jdata = []
    count = 5
    for entry in allposts:
        jdata.append(entry.getDict())
        count -= 1
        if count == 0:
            break
    return SuccessRes(data = jdata)



@require_POST
@login_required
@csrf_exempt
@kuzines_api
def getProfile(request):
    """
    required paras:
    string username
    """
    # problem: picture cannot be encoded in json package
    # friends_set not found
    if request.DATA.has_key('username'):
        username = request.DATA['username']
    else:
        return FailResWithMsg("username not found")

    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return FailResWithMsg("User not exists")


    allposts = user.posts_set.all()
    jdata = [{
        'username' : username,
        'photo' : '/'.join([HttpRequest.get_host(request), user.myuserinfo.photo.url]),
        # 'numOfFriends' : user.friends_set.count(),
        'numOfFavRests' : user.favrestaurants_set.count(),
        'numOfFavDishes' : user.favdishes_set.count(),
        'numOfChickIn' : user.checkins_set.count(),
        'numOfUsertags' : user.usertags_set.count(),
        'numOfReviews' : user.reviews_set.count(),
        'numOfLikes' : user.likes_set.count(),
        'numOfTries' : user.tries_set.count(),
    }]
    return SuccessRes(data = jdata)



@require_POST
@login_required
@csrf_exempt
@kuzines_api
def uploadFile(request):
    """ required_paras
    FileField FILES['file']
    request.user exists
        output_json
    file location is at MEDIA_ROOT + profile_file_name (see in models)
    file url is at MEDIA_URL(?) + urls + profile_file_name (see in urls.py)
    """
    # not sure: assume all paras are valid
    user = request.user
    if request.FILES.has_key('file'):
        user.myuserinfo.photo = request.FILES['file']
        user.myuserinfo.save()
        return SuccessRes(message = '/'.join([HttpRequest.get_host(request), user.myuserinfo.photo.url]) )
    else:
        return FailResWithMsg("Error retriving the file")




from .models import Dishes

@require_POST
@login_required
@csrf_exempt
@kuzines_api
#function for user checking in at a resteraunt 
def getReviews(request):
    #TODO: set the parameter: username, resterauntID
    """ 
    required_paras
    string keyword
    string mode = "my" or "all"
    """
    if request.DATA.has_key('keyword'):
        keyword = request.DATA['keyword']
    else:
        return FailResWithMsg("Keyword not found")
    if request.DATA.has_key('mode'):
        mode = request.DATA['mode']
    else:
        return FailResWithMsg("Mode not found")
    if mode == "my":
        dishesset = request.user.reviews_set.filter(did__name__contains = keyword)
    elif mode == "all":
        dishesset = Dishes.objects.filter(name__contains = keyword)
    else:
        return FailResWithMsg("Mode not valid")

    jdata = []
    for entry in dishesset:
        tmp = {}
        tmp['dish_name'] = entry.name
        tmp['resteraunt_name'] = entry.resteraunt.name
        jdata.append(tmp)

    return SuccessRes(data = jdata)





from .models import Restaurants

@require_POST
@login_required
@csrf_exempt
@kuzines_api
def newRestaurant(request):
    """
    required paras:
    string name
    optional paras:
    string type
    *location location
    """
    #TODO: location not accomplished
    # one problem remain: what content includes quotation marks
    if request.DATA.has_key('name'):
        name = request.DATA['name']
    else:
        return FailResWithMsg("name not found")

    newRest = Restaurants(name = name)
    if request.DATA.has_key('type'):
        newtype = request.DATA['type']
        newRest.type = newtype
    newRest.save()
    return SuccessRes(message = "New resturant added")






def SuccessRes(data = "", message = ""):
    res = RSuccess()
    res.data = data
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")

def FailResWithMsg(message):
    res = RFail()
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")

def ErrorRes(message):
    res = RError()
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")
