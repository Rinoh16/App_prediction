from functools import wraps
from django.shortcuts import redirect

def login_required_session(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('login')  # ou l'URL nommée de ta vue login
        return view_func(request, *args, **kwargs)
    return wrapper
