from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context, loader

def index(request):

    print('login:')
    print(request.user.is_authenticated())

    if request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        template = loader.get_template('login.html')
        context = Context({
            'test': 'test',
        })
        return HttpResponse(template.render(context))