from django.conf import settings

def get_context(title,active):
    return {"title":title,"active":active, "debug_flag": settings.DEBUG}


def get_context_back(context,title,active):
    c = context
    c["title"] = title
    c["active"] = active
    c["debug-flag"] = settings.DEBUG
    return c