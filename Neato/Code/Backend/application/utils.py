from functools import wraps
from flask import current_app
from datetime import datetime
from flask_caching import Cache


# Create a global cache instance
cache = Cache()

class CacheManager:
    """Centralized cache management for the application"""
    
    @staticmethod
    def init_app(app):
        """Initialize the cache with the Flask app"""
        cache.init_app(app)
        return cache

    @staticmethod
    def get_cache():
        """Get the cache instance"""
        return cache

    @staticmethod
    def make_key(*args, **kwargs):
        """Generate a standard cache key"""
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return "neato:" + ":".join(key_parts)

    @classmethod
    def cached(cls, timeout=300, key_prefix=''):
        """Custom caching decorator"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                cache = cls.get_cache()
                cache_key = cls.make_key(key_prefix, f.__name__, *args, **kwargs)
                
                # Get from cache
                cached_value = cache.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # If not in cache, execute function
                value = f(*args, **kwargs)
                
                # Store in cache
                cache.set(cache_key, value, timeout=timeout)
                return value
            return decorated_function
        return decorator

    @classmethod
    def clear_user_caches(cls, user_id):
        """Clear all caches related to a user"""
        cache = cls.get_cache()
        keys_to_delete = [
            cls.make_key('user', user_id),
            cls.make_key('requests', user_id),
            cls.make_key('search', user_id)
        ]
        for key in keys_to_delete:
            cache.delete(key)

    @classmethod
    def clear_service_caches(cls, service_id=None):
        """Clear service-related caches"""
        cache = cls.get_cache()
        if service_id:
            cache.delete(cls.make_key('service', service_id))
        cache.delete(cls.make_key('services', 'all'))

    @classmethod
    def clear_request_caches(cls, request_id=None, user_id=None):
        """Clear service request related caches"""
        cache = cls.get_cache()
        if request_id:
            cache.delete(cls.make_key('request', request_id))
        if user_id:
            cache.delete(cls.make_key('requests', user_id))
        cache.delete(cls.make_key('requests', 'all'))



