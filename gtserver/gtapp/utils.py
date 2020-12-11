from django.conf import settings

def get_context(title,active):
    return {"title":title,"active":active, "debug_flag": settings.DEBUG}


