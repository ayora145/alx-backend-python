
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Simple subclass if you later need custom behavior.
    Currently, this inherits all behavior from simplejwt.
    """
    pass
