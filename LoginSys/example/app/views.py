from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from social.backends.google import GooglePlusAuth


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return render_to_response('home.html', {
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
    }, RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
    return render_to_response('done.html', {
        'user': request.user,
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': scope
    }, RequestContext(request))


def signup_email(request):
    return render_to_response('email_signup.html', {}, RequestContext(request))


def validation_sent(request):
    return render_to_response('validation_sent.html', {
        'email': request.session.get('email_validation_address')
    }, RequestContext(request))


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))

#############################################################

from django.contrib.auth import logout as auth_logout
# from django.http import HttpResponseRedirect

def mylogout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('home')
    # return HttpResponseRedirect('/login/')

########################################################

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from jsend import RSuccess, RFail, RError
from django.contrib import auth
import datetime
import json

@csrf_exempt
def mylogin(request):
    if request.method != 'POST':
        return FailResWithMsg("POST method expected")
    if request.POST.has_key('username') and request.POST.has_key('password'):
        username = request.POST['username']
        password = request.POST['password']
    else:
        return FailResWithMsg("username or password not found")
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth.login(request, user)
        res = RSuccess()
        res.message = "Login success"
        res.code = 200
        date_login_expiring = datetime.datetime.now() + datetime.timedelta(weeks = 2)
        res.data['username'] = username
        res.data['data_login_expiring'] = FormattedTime(date_login_expiring)
        return redirect('done', {
            'json': json.dumps(res),
            'user': user,
            })
        # return HttpResponse(json.dumps(res), content_type = "application/json")
    else:
        return FailResWithMsg("username and password dismatch")

def match(username, password):
    return True

def FormattedTime(time):
    return time.isoformat()
    
def hello(request):
    return HttpResponse("Hello world")

def FailResWithMsg(message):
    res = RFail()
    res.message = message
    return HttpResponse(json.dumps(res), content_type = "application/json")
########################################################