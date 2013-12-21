"""
Decorators for api
"""
import json
import re

json_matcher = re.compile("^(application|text)/(|x-)json")
def kuzines_api(var = "DATA", allow_get = False):
	"""
	Kuzines API Decorator
	Generates DATA tag from request JSON if given
	Handles output content type to indicate jsend data content
	"""

	def wrapper(func):
		def handler(request):
			setattr(request, var, None)
			if request.method == "POST":
				if json_matcher.match(request.META['CONTENT_TYPE'] or ""):
					setattr(request, var, json.loads(request.body))
				else:
					setattr(request, var, request.POST)
			elif request.method == "GET" and allow_get:
				setattr(request, var, request.GET)

			#Change output content type
			response = func(request)
			response['Content-Type'] = "application/json;jsend=1"
			return response

		return handler

	if callable(var):
		func = var
		var = "DATA"
		return wrapper(func)

	return wrapper