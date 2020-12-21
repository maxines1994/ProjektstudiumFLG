from django.conf import settings

#Global context

def gtcontext(request):
    if request.user.groups.filter(name='JOGA').exists():
        company = 'joga' # light-blue
    elif request.user.groups.filter(name='suppliers').exists():
        company = 'supplier' # green
    elif request.user.groups.filter(name='customers').exists():
        company = 'customer' # red
    else:
        company = 'none' # grey


    return {"debug_flag": settings.DEBUG, "company": company}