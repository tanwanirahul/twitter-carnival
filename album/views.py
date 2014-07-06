from django.http.response import HttpResponseRedirect


# Create your views here.
def index(request):
    '''
        Handles the main landing page.
    '''
    return HttpResponseRedirect("/static/templates/index.html")
