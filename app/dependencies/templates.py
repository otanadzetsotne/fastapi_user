from functools import cache

from fastapi.templating import Jinja2Templates


@cache
def get_templates():
    return Jinja2Templates(directory='templates')
