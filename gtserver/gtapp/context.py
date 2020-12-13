from django.conf import settings

#Global context

def gtcontext(request):
    return {"debug_flag": settings.DEBUG}