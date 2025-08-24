from fastapi import FastAPI, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Optional, List
import uuid
from datetime import datetime

from database import get_db, init_db
from models import *
from services import (
    UserService, SituationService, SessionService, 
    MessageService, AIPersonaService, FeedbackService
)
from config import settings

app = FastAPI(title=settings.APP_NAME)

# Initialize database
init_db()

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
user_service = UserService()
situation_service = SituationService()
session_service = SessionService()
message_service = MessageService()
ai_service = AIPersonaService()
feedback_service = FeedbackService()

# Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user_uuid: Optional[str] = None):
    """Home page with situation selection"""
    try:
        # Get or create user
        user = await user_service.create_or_get_user(user_uuid)
        
        # Get all situations grouped by category
        situations = await situation_service.get_all_situations()
        
        # Group situations by category
        categories = {}
        for situation in situations:
            if situation.category not in categories:
                categories[situation.category] = []
            categories[situation.category].append(situation)
        
        return templates.TemplateResponse("home.html", {
            "request": request,
            "user": user,
            "categories": categories,
            "app_name": settings.APP_NAME
        })
    except Exception as e:
        print(f"Error in home route: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load roleplay situations. Please try again."
        })

@app.post("/start-session")
async def start_session(
    request: Request,
    situation_id: int = Form(...),
    user_uuid: str = Form(...)
):
    """Start a new roleplay session"""
    try:
        # Get user
        user = await user_service.create_or_get_user(user_uuid)
        
        # Create new session
        session = await session_service.create_session(str(user.id), situation_id)
        
        if not session:
            raise HTTPException(status_code=400, detail="Unable to create session")
        
        # Redirect to chat interface
        return RedirectResponse(url=f"/session/{session.id}?user_uuid={user.session_uuid}", status_code=303)
        
    except Exception as e:
        print(f"Error starting session: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to start roleplay session. Please try again."
        })

@app.get("/session/{session_id}", response_class=HTMLResponse)
async def chat_interface(request: Request, session_id: str, user_uuid: str):
    """Chat interface for roleplay session"""
    try:
        # Enhanced user and session validation
        user = await user_service.create_or_get_user(user_uuid)
        if not user:
            print(f"Failed to create/get user for UUID: {user_uuid}")
            raise HTTPException(status_code=403, detail="User session invalid")
        
        session_data = await session_service.get_session_with_messages(session_id)
        if not session_data:
            print(f"Session not found: {session_id}")
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Verify user owns this session
        if str(session_data.user_id) != str(user.id):
            print(f"Session ownership mismatch: session.user_id={session_data.user_id}, user.id={user.id}")
            raise HTTPException(status_code=403, detail="Access denied - session belongs to different user")
        
        # Verify session is still active
        if session_data.status not in ['active', 'completed']:
            print(f"Invalid session status: {session_data.status}")
            raise HTTPException(status_code=400, detail="Session is not accessible")
        
        # If no messages yet, generate AI opening message
        if not session_data.messages:
            try:
                opening_message = await ai_service.generate_response(session_data.situation, [])
                await message_service.add_message(session_id, "persona", opening_message)
                # Refresh session data
                session_data = await session_service.get_session_with_messages(session_id)
                print(f"Generated opening message for session {session_id}")
            except Exception as e:
                print(f"Error generating opening message: {e}")
                # Continue without opening message - user can start the conversation
        
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "session": session_data,
            "user": user,
            "app_name": settings.APP_NAME
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat interface: {e}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load chat session. Please try again."
        })

@app.post("/session/{session_id}/message")
async def send_message(
    session_id: str,
    message: str = Form(...),
    user_uuid: str = Form(...)
):
    """Send a message in the chat session"""
    try:
        # Input validation
        if not message or not message.strip():
            return JSONResponse({"error": "Message cannot be empty"}, status_code=400)
        
        if len(message.strip()) > 1000:
            return JSONResponse({"error": "Message too long (max 1000 characters)"}, status_code=400)
        
        # Enhanced user and session validation
        user = await user_service.create_or_get_user(user_uuid)
        if not user:
            return JSONResponse({"error": "Invalid user session"}, status_code=403)
        
        session_data = await session_service.get_session_with_messages(session_id)
        if not session_data:
            return JSONResponse({"error": "Session not found"}, status_code=404)
        
        # Verify user owns this session
        if str(session_data.user_id) != str(user.id):
            print(f"Message send - ownership mismatch: session.user_id={session_data.user_id}, user.id={user.id}")
            return JSONResponse({"error": "Access denied"}, status_code=403)
        
        # Verify session is active
        if session_data.status != 'active':
            return JSONResponse({"error": "Session is no longer active"}, status_code=400)
        
        # Check message limit per session
        current_user_messages = len([msg for msg in session_data.messages if msg.message_type == 'user'])
        if current_user_messages >= settings.MAX_MESSAGES_PER_SESSION:
            return JSONResponse({"error": "Message limit reached for this session"}, status_code=400)
        
        # Add user message
        user_message = await message_service.add_message(session_id, "user", message.strip())
        if not user_message:
            return JSONResponse({"error": "Failed to save user message"}, status_code=500)
        
        # Update user activity
        await user_service.update_last_active(str(user.id))
        
        # Generate AI response
        try:
            updated_messages = await message_service.get_session_messages(session_id)
            ai_response = await ai_service.generate_response(session_data.situation, updated_messages)
            
            # Add AI message
            ai_message = await message_service.add_message(session_id, "persona", ai_response)
            
            return JSONResponse({
                "success": True,
                "user_message": {
                    "id": str(user_message.id),
                    "content": user_message.content,
                    "timestamp": user_message.timestamp.isoformat()
                },
                "ai_message": {
                    "id": str(ai_message.id) if ai_message else None,
                    "content": ai_response,
                    "timestamp": ai_message.timestamp.isoformat() if ai_message else datetime.now().isoformat()
                }
            })
            
        except Exception as ai_error:
            print(f"Error generating AI response: {ai_error}")
            # Return user message even if AI response fails
            return JSONResponse({
                "success": True,
                "user_message": {
                    "id": str(user_message.id),
                    "content": user_message.content,
                    "timestamp": user_message.timestamp.isoformat()
                },
                "ai_message": {
                    "id": None,
                    "content": "I'm having trouble responding right now. Please try sending another message.",
                    "timestamp": datetime.now().isoformat()
                }
            })
        
    except Exception as e:
        print(f"Error sending message: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": "Failed to send message. Please try again."}, status_code=500)

@app.post("/session/{session_id}/end")
async def end_session(
    session_id: str,
    user_uuid: str = Form(...)
):
    """End the roleplay session and generate feedback"""
    try:
        # Verify user owns this session
        user = await user_service.create_or_get_user(user_uuid)
        session_data = await session_service.get_session_with_messages(session_id)
        
        if not session_data or str(session_data.user_id) != str(user.id):
            return JSONResponse({"error": "Session not found or access denied"}, status_code=403)
        
        # End the session
        success = await session_service.end_session(session_id)
        if not success:
            return JSONResponse({"error": "Failed to end session"}, status_code=500)
        
        # Generate feedback
        feedback = await feedback_service.generate_session_feedback(session_id)
        
        return JSONResponse({
            "success": True,
            "redirect_url": f"/session/{session_id}/feedback?user_uuid={user.session_uuid}"
        })
        
    except Exception as e:
        print(f"Error ending session: {e}")
        return JSONResponse({"error": "Failed to end session"}, status_code=500)

@app.get("/session/{session_id}/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request, session_id: str, user_uuid: str):
    """Display session feedback and analysis"""
    try:
        # Verify user owns this session
        user = await user_service.create_or_get_user(user_uuid)
        session_data = await session_service.get_session_with_messages(session_id)
        
        if not session_data or str(session_data.user_id) != str(user.id):
            raise HTTPException(status_code=403, detail="Session not found or access denied")
        
        return templates.TemplateResponse("feedback.html", {
            "request": request,
            "session": session_data,
            "user": user,
            "app_name": settings.APP_NAME
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in feedback page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load feedback. Please try again."
        })

@app.get("/history", response_class=HTMLResponse)
async def session_history(request: Request, user_uuid: str):
    """Display user's session history"""
    try:
        # Get user
        user = await user_service.create_or_get_user(user_uuid)
        
        # Get user's sessions
        sessions = await session_service.get_user_sessions(str(user.id))
        
        return templates.TemplateResponse("history.html", {
            "request": request,
            "sessions": sessions,
            "user": user,
            "app_name": settings.APP_NAME
        })
        
    except Exception as e:
        print(f"Error in session history: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load session history. Please try again."
        })

@app.get("/session/{session_id}/review", response_class=HTMLResponse)
async def review_session(request: Request, session_id: str, user_uuid: str):
    """Review a completed session with full transcript"""
    try:
        # Verify user owns this session
        user = await user_service.create_or_get_user(user_uuid)
        session_data = await session_service.get_session_with_messages(session_id)
        
        if not session_data or str(session_data.user_id) != str(user.id):
            raise HTTPException(status_code=403, detail="Session not found or access denied")
        
        return templates.TemplateResponse("review.html", {
            "request": request,
            "session": session_data,
            "user": user,
            "app_name": settings.APP_NAME
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in review session: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load session review. Please try again."
        })

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error": "Page not found. Please check the URL and try again."
    }, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error": "An internal error occurred. Please try again later."
    }, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)