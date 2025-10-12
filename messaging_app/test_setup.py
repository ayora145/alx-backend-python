#!/usr/bin/env python3
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.insert(0, '/app')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

try:
    django.setup()
    print("✅ Django setup successful")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    print("✅ Database connection successful")
    
    # Test imports
    from chats.models import User, Conversation, Message
    print("✅ Models imported successfully")
    
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)