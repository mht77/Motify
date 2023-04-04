from django.core.cache import cache

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def use_cache(func):
    def wrapper(viewClass, *args, **kwargs):
        key = func.__name__ + type(viewClass).__name__
        if kwargs.get('pk'):
            key += str(kwargs['pk'])
        print(key)
        try:
            date = cache.get(key)
            if date:
                return Response(date, status=status.HTTP_200_OK)
        except KeyError:
            pass
        except ValueError:
            pass
        except Exception as e:
            print(e)
        res = func(viewClass, *args, **kwargs)
        res.accepted_renderer = JSONRenderer()
        res.accepted_media_type = "application/json"
        res.renderer_context = {}
        res.render()
        cache.set(key, res.data)
        return res

    wrapper.__wrapped__ = func
    return wrapper
