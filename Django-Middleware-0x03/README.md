# Django Middleware Chat Application

This Django application demonstrates four custom middleware implementations for a messaging/chat system.

## Middleware Implemented

### 1. RequestLoggingMiddleware
- Logs all user requests to `requests.log`
- Format: `{timestamp} - User: {user} - Path: {request.path}`

### 2. RestrictAccessByTimeMiddleware  
- Restricts chat access to 6 PM - 9 PM only
- Returns 403 Forbidden outside these hours

### 3. OffensiveLanguageMiddleware
- Rate limiting: 5 messages per minute per IP address
- Blocks further messaging if limit exceeded

### 4. RolePermissionMiddleware
- Requires admin or moderator role for chat access
- Returns 403 Forbidden for regular users

## Setup Instructions

1. Run migrations:
   ```bash
   python manage.py migrate
   ```

2. Start the server:
   ```bash
   python manage.py runserver
   ```

3. Test users created:
   - Admin: `admin` / `admin123` (role: admin)
   - Regular: `testuser` / `test123` (role: user)

## Testing the Middleware

1. **Request Logging**: Check `requests.log` file after making requests
2. **Time Restriction**: Access `/chats/` outside 6-9 PM to see restriction
3. **Rate Limiting**: Send more than 5 POST requests within a minute
4. **Role Permission**: Login as `testuser` to see access denied

## URLs
- `/` - Home page
- `/chats/` - Chat interface (requires login)
- `/admin/` - Admin interface
- `/accounts/login/` - Login page