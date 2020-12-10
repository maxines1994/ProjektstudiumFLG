from django.conf import settings

def get_context(title,active):
    return {"title":title,"active":active, "debug": settings.DEBUG}


