from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context, loader

def index(request):

    print('exp:')
    print(request.user.is_authenticated())

    if request.user.is_authenticated():
        template = loader.get_template('groupboard.html')
        context = Context({
            'test': 'test',
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('/accounts/login/')