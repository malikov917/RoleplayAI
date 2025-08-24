# AI Roleplay Trainer - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
The application uses anonymous session tracking via UUID. No authentication required.

## Core Endpoints

### 1. Homepage
```http
GET /
```

**Parameters:**
- `user_uuid` (optional): String - User session UUID for returning users

**Response:** HTML page with scenario selection

**Example:**
```bash
curl "http://localhost:8000/?user_uuid=123e4567-e89b-12d3-a456-426614174000"
```

### 2. Start Roleplay Session
```http
POST /start-session
```

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
- `situation_id` (required): Integer - ID of the roleplay scenario
- `user_uuid` (required): String - User session UUID

**Response:** Redirect (303) to chat interface

**Example:**
```bash
curl -X POST "http://localhost:8000/start-session" \
  -d "situation_id=1&user_uuid=123e4567-e89b-12d3-a456-426614174000"
```

### 3. Chat Interface
```http
GET /session/{session_id}
```

**Parameters:**
- `session_id` (path): String - UUID of the roleplay session
- `user_uuid` (query): String - User session UUID

**Response:** HTML chat interface

**Example:**
```bash
curl "http://localhost:8000/session/456e7890-e89b-12d3-a456-426614174000?user_uuid=123e4567-e89b-12d3-a456-426614174000"
```

### 4. Send Message
```http
POST /session/{session_id}/message
```

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
- `session_id` (path): String - UUID of the roleplay session
- `message` (body): String - User's message content
- `user_uuid` (body): String - User session UUID

**Response:** JSON with user and AI messages

**Response Format:**
```json
{
  "user_message": {
    "id": "msg-uuid",
    "content": "Hello, I'm excited to interview for this position.",
    "timestamp": "2025-07-17T21:30:00Z"
  },
  "ai_message": {
    "id": "ai-msg-uuid", 
    "content": "Great! Let's start with you telling me about yourself.",
    "timestamp": "2025-07-17T21:30:02Z"
  }
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/session/456e7890-e89b-12d3-a456-426614174000/message" \
  -d "message=Hello!&user_uuid=123e4567-e89b-12d3-a456-426614174000"
```

### 5. End Session
```http
POST /session/{session_id}/end
```

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
- `session_id` (path): String - UUID of the roleplay session
- `user_uuid` (body): String - User session UUID

**Response:** JSON with feedback page URL

**Response Format:**
```json
{
  "success": true,
  "redirect_url": "/session/456e7890-e89b-12d3-a456-426614174000/feedback?user_uuid=123e4567-e89b-12d3-a456-426614174000"
}
```

### 6. View Feedback
```http
GET /session/{session_id}/feedback
```

**Parameters:**
- `session_id` (path): String - UUID of the roleplay session
- `user_uuid` (query): String - User session UUID

**Response:** HTML feedback page with performance analysis

### 7. Session Review
```http
GET /session/{session_id}/review
```

**Parameters:**
- `session_id` (path): String - UUID of the roleplay session
- `user_uuid` (query): String - User session UUID

**Response:** HTML page with full conversation transcript

### 8. Session History
```http
GET /history
```

**Parameters:**
- `user_uuid` (query): String - User session UUID

**Response:** HTML page with list of user's past sessions

### 9. Health Check
```http
GET /health
```

**Response:** JSON health status

**Response Format:**
```json
{
  "status": "healthy",
  "app": "AI Roleplay Trainer"
}
```

## Data Models

### User
```json
{
  "id": "user-uuid",
  "session_uuid": "session-uuid", 
  "created_at": "2025-07-17T21:00:00Z",
  "last_active": "2025-07-17T21:30:00Z"
}
```

### Situation
```json
{
  "id": 1,
  "title": "Job Interview - Software Developer",
  "description": "Practice answering common technical and behavioral questions...",
  "persona_script": "You are Sarah Chen, a Senior Engineering Manager...",
  "difficulty_level": "intermediate",
  "category": "career",
  "created_at": "2025-07-17T20:00:00Z",
  "is_active": true
}
```

### Roleplay Session
```json
{
  "id": "session-uuid",
  "user_id": "user-uuid",
  "situation_id": 1,
  "started_at": "2025-07-17T21:00:00Z",
  "ended_at": "2025-07-17T21:15:00Z",
  "status": "completed",
  "session_duration": 900
}
```

### Dialogue Message
```json
{
  "id": "message-uuid",
  "session_id": "session-uuid",
  "message_type": "user", // or "persona"
  "content": "I have 5 years of experience in Python development...",
  "timestamp": "2025-07-17T21:05:00Z",
  "message_order": 3
}
```

### Session Summary
```json
{
  "id": "summary-uuid",
  "session_id": "session-uuid",
  "performance_score": 78,
  "feedback_text": "Your interview performance showed high engagement...",
  "strengths": "Good use of specific examples • Clear communication style",
  "improvement_areas": "Practice the STAR method • Research company background",
  "key_insights": "Focus on demonstrating cultural fit • Prepare technical examples",
  "created_at": "2025-07-17T21:16:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Unable to create session"
}
```

### 403 Forbidden
```json
{
  "detail": "Session not found or access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Page not found. Please check the URL and try again."
}
```

### 500 Internal Server Error
```json
{
  "detail": "An internal error occurred. Please try again later."
}
```

## Rate Limits

Currently no rate limiting implemented. Recommended for production:
- 100 requests per minute per IP
- 10 session creations per hour per IP
- 5 message sends per minute per session

## Available Scenarios

| ID | Title | Category | Difficulty |
|----|-------|----------|------------|
| 1 | Job Interview - Software Developer | career | intermediate |
| 2 | Difficult Customer Service | customer_service | advanced |
| 3 | Asking for a Raise | career | intermediate |
| 4 | First Date Conversation | social | beginner |
| 5 | Giving Constructive Feedback | management | advanced |
| 6 | Networking Event Small Talk | networking | beginner |

## Integration Examples

### JavaScript Integration
```javascript
// Start a new session
async function startSession(situationId, userUuid) {
  const formData = new FormData();
  formData.append('situation_id', situationId);
  formData.append('user_uuid', userUuid);
  
  const response = await fetch('/start-session', {
    method: 'POST',
    body: formData
  });
  
  // Will redirect to chat interface
}

// Send a message
async function sendMessage(sessionId, message, userUuid) {
  const formData = new FormData();
  formData.append('message', message);
  formData.append('user_uuid', userUuid);
  
  const response = await fetch(`/session/${sessionId}/message`, {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}
```

### Python Integration
```python
import requests

# Start session
response = requests.post('http://localhost:8000/start-session', {
    'situation_id': 1,
    'user_uuid': 'your-user-uuid'
})

# Send message
response = requests.post(
    f'http://localhost:8000/session/{session_id}/message',
    {
        'message': 'Hello, I am interested in this position.',
        'user_uuid': 'your-user-uuid'
    }
)

result = response.json()
ai_response = result['ai_message']['content']
```

## Testing Endpoints

### Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","app":"AI Roleplay Trainer"}
```

### Homepage Access
```bash
curl -I http://localhost:8000/
# Expected: HTTP/1.1 200 OK
```

### Session Creation Flow
```bash
# 1. Get homepage with new user
curl "http://localhost:8000/"

# 2. Extract user UUID from response
# 3. Start session
curl -X POST "http://localhost:8000/start-session" \
  -d "situation_id=1&user_uuid=extracted-uuid"

# 4. Follow redirect to chat interface
# 5. Send messages and test conversation flow
```