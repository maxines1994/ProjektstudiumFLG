from django.conf import settings

def get_context(title,active):
    return {"title":title,"active":active}

def get_context_back(context,title,active):
    c = context
    c["title"] = title
    c["active"] = active
    return c