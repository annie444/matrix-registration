from flask import request
from flask_limiter import Limiter

from . import config


def get_real_user_ip() -> str:
    """ratelimit the users original ip instead of (optional) reverse proxy"""
    return next(iter(request.headers.getlist("X-Forwarded-For")), request.remote_addr)


def get_default_rate_limit() -> str:
    """return limit_string"""
    return "; ".join(config.config.rate_limit)

def get_limiter() -> Limiter:
    """return limiter object"""
    kwargs = {
        "key_func": get_real_user_ip,
        "app": None,
    }


    if hasattr(config.config, "memcached") and config.config.memcached is not None and config.config.memcached.uri is not None and config.config.memcached.uri != "":
        kwargs["storage_uri"] = config.config.memcached.uri
        if config.config.memcached.options is not None:
            kwargs["storage_options"] = config.config.memcached.options
    elif hasattr(config.config, "redis") and config.config.redis is not None and config.config.redis.uri is not None and config.config.redis.uri != "":
        kwargs["storage_uri"] = config.config.redis.uri
        if config.config.redis.options is not None:
           kwargs["storage_options"] = config.config.redis.options
        if config.config.redis.strategy is not None:
            kwargs["strategy"] = config.config.redis.strategy
    elif hasattr(config.config, "mongodb") and config.config.mongodb is not None and config.config.mongodb.uri is not None and config.config.mongodb.uri != "":
        kwargs["storage_uri"] = config.config.mongodb.uri
        if config.config.mongodb.options is not None:
           kwargs["storage_options"] = config.config.mongodb.options
        if config.config.mongodb.strategy is not None:
            kwargs["strategy"] = config.config.mongodb.strategy
    return Limiter(**kwargs)

limiter = get_limiter()
