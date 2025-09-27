import logging
import os
from datetime import datetime, time
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

# Configure logging for request logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(18, 0)  # 6 PM
        end_time = time(21, 0)    # 9 PM
        
        if request.path.startswith('/chats/') and not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Chat access is restricted outside 6 PM - 9 PM")
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = defaultdict(list)
        self.max_requests = 5
        self.time_window = 60  # 1 minute in seconds

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            client_ip = self.get_client_ip(request)
            current_time = datetime.now().timestamp()
            
            # Clean old requests outside time window
            self.ip_requests[client_ip] = [
                req_time for req_time in self.ip_requests[client_ip]
                if current_time - req_time < self.time_window
            ]
            
            # Check if limit exceeded
            if len(self.ip_requests[client_ip]) >= self.max_requests:
                return HttpResponseForbidden("Rate limit exceeded. Too many messages sent.")
            
            # Add current request
            self.ip_requests[client_ip].append(current_time)
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/') and request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied. Admin or moderator role required.")
        
        response = self.get_response(request)
        return response