
import functools
import warnings

def deprecated(reason=''):
    def decorator(cls_or_func):
        msg = f"This call is deprecated and will be removed in a future version. Reason: {reason}"

        @functools.wraps(cls_or_func)
        def new_func(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return cls_or_func(*args, **kwargs)

        return new_func
    return decorator


def todo(reason=''):
    def decorator(cls_or_func):
        msg = f"This call is not implemented yet. Reason: {reason}"

        @functools.wraps(cls_or_func)
        def new_func(*args, **kwargs):
            warnings.warn(msg, category=PendingDeprecationWarning, stacklevel=2)
            return cls_or_func(*args, **kwargs)

        return new_func
    return decorator
