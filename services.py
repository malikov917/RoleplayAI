import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
import dateutil.parser
from database import get_supabase_client
from models import (
    User, UserCreate, Situation, RoleplaySession, RoleplaySessionCreate,
    DialogueMessage, DialogueMessageCreate, SessionSummary, SessionSummaryCreate,
    SessionWithSituation, SessionWithMessages
)
from config import settings
import json
import random
import openai
import asyncio

class UserService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def create_or_get_user(self, session_uuid: Optional[str] = None) -> Optional[User]:
        """Create a new anonymous user or get existing one by session UUID"""
        try:
            if session_uuid:
                # Try to get existing user with better error handling
                try:
                    response = self.supabase.table('users').select('*').eq('session_uuid', session_uuid).maybe_single().execute()
                    if response and response.data:
                        # Update last active time
                        self.supabase.table('users').update({
                            'last_active': datetime.now().isoformat()
                        }).eq('session_uuid', session_uuid).execute()
                        
                        return User(**response.data)
                except Exception as e:
                    print(f"Error fetching existing user: {e}")
            
            # Create new user with validation
            new_uuid = str(uuid.uuid4())
            current_time = datetime.now(timezone.utc).isoformat()
            
            user_data = {
                'session_uuid': new_uuid,
                'created_at': current_time,
                'last_active': current_time
            }
            
            response = self.supabase.table('users').insert(user_data).execute()
            if response and response.data and len(response.data) > 0:
                print(f"Created new user with session_uuid: {new_uuid}")
                return User(**response.data[0])
            
            raise Exception(f"Failed to create user - response: {response}")
            
        except Exception as e:
            print(f"Critical error in create_or_get_user: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_user_by_session_uuid(self, session_uuid: str) -> Optional[User]:
        """Get user by session UUID with validation"""
        try:
            response = self.supabase.table('users').select('*').eq('session_uuid', session_uuid).maybe_single().execute()
            if response and response.data:
                return User(**response.data)
            return None
        except Exception as e:
            print(f"Error getting user by session UUID: {e}")
            return None
    
    async def validate_user_session(self, user_id: str, session_uuid: str) -> bool:
        """Validate that user_id matches session_uuid"""
        try:
            response = self.supabase.table('users').select('id').eq('session_uuid', session_uuid).eq('id', user_id).maybe_single().execute()
            return response and response.data is not None
        except Exception as e:
            print(f"Error validating user session: {e}")
            return False
    
    async def update_last_active(self, user_id: str) -> None:
        """Update user's last active timestamp"""
        try:
            self.supabase.table('users').update({
                'last_active': datetime.now(timezone.utc).isoformat()
            }).eq('id', user_id).execute()
        except Exception as e:
            print(f"Error updating last active: {e}")

class SituationService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def get_all_situations(self) -> List[Situation]:
        """Get all active situations"""
        try:
            response = self.supabase.table('situations').select('*').eq('is_active', True).order('category, difficulty_level, title').execute()
            return [Situation(**item) for item in response.data]
        except Exception as e:
            print(f"Error getting situations: {e}")
            return []
    
    async def get_situation_by_id(self, situation_id: int) -> Optional[Situation]:
        """Get situation by ID"""
        try:
            response = self.supabase.table('situations').select('*').eq('id', situation_id).maybe_single().execute()
            if response.data:
                return Situation(**response.data)
            return None
        except Exception as e:
            print(f"Error getting situation {situation_id}: {e}")
            return None

class SessionService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def create_session(self, user_id: str, situation_id: int) -> Optional[RoleplaySession]:
        """Create a new roleplay session with validation"""
        try:
            # Validate inputs
            if not user_id or not situation_id:
                print(f"Invalid session creation parameters: user_id={user_id}, situation_id={situation_id}")
                return None
            
            # Verify user exists
            user_check = self.supabase.table('users').select('id').eq('id', user_id).maybe_single().execute()
            if not user_check or not user_check.data:
                print(f"User {user_id} not found for session creation")
                return None
            
            # Verify situation exists
            situation_check = self.supabase.table('situations').select('id').eq('id', situation_id).eq('is_active', True).maybe_single().execute()
            if not situation_check or not situation_check.data:
                print(f"Situation {situation_id} not found or inactive")
                return None
            
            # Check for existing active session
            existing_session = self.supabase.table('roleplay_sessions').select('id').eq('user_id', user_id).eq('status', 'active').maybe_single().execute()
            if existing_session and existing_session.data:
                print(f"User {user_id} already has an active session: {existing_session.data['id']}")
                # Optionally end the existing session or return it
            
            session_data = {
                'user_id': user_id,
                'situation_id': situation_id,
                'status': 'active',
                'started_at': datetime.now(timezone.utc).isoformat()
            }
            
            response = self.supabase.table('roleplay_sessions').insert(session_data).execute()
            if response and response.data and len(response.data) > 0:
                print(f"Created session {response.data[0]['id']} for user {user_id}")
                return RoleplaySession(**response.data[0])
            
            print(f"Failed to create session - response: {response}")
            return None
            
        except Exception as e:
            print(f"Error creating session: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_user_sessions(self, user_id: str) -> List[SessionWithSituation]:
        """Get all sessions for a user with situation details"""
        try:
            response = self.supabase.table('roleplay_sessions').select('*').eq('user_id', user_id).order('started_at', desc=True).execute()
            
            sessions = []
            for session_data in response.data:
                # Get situation details
                situation_response = self.supabase.table('situations').select('*').eq('id', session_data['situation_id']).maybe_single().execute()
                
                # Get message count
                message_count_response = self.supabase.table('dialogue_messages').select('id', count='exact').eq('session_id', session_data['id']).execute()
                message_count = message_count_response.count if message_count_response.count else 0
                
                session = SessionWithSituation(
                    **session_data,
                    situation=Situation(**situation_response.data) if situation_response.data else None,
                    message_count=message_count
                )
                sessions.append(session)
            
            return sessions
        except Exception as e:
            print(f"Error getting user sessions: {e}")
            return []
    
    async def get_session_with_messages(self, session_id: str) -> Optional[SessionWithMessages]:
        """Get session with all messages and summary"""
        try:
            # Get session
            session_response = self.supabase.table('roleplay_sessions').select('*').eq('id', session_id).maybe_single().execute()
            if not session_response or not session_response.data:
                print(f"Session {session_id} not found")
                return None
            
            # Get situation
            situation_response = self.supabase.table('situations').select('*').eq('id', session_response.data['situation_id']).maybe_single().execute()
            if not situation_response or not situation_response.data:
                print(f"Situation {session_response.data['situation_id']} not found")
                return None
            
            # Get messages
            messages_response = self.supabase.table('dialogue_messages').select('*').eq('session_id', session_id).order('message_order').execute()
            messages_data = messages_response.data if messages_response and messages_response.data else []
            
            # Get summary
            summary_response = self.supabase.table('session_summaries').select('*').eq('session_id', session_id).maybe_single().execute()
            summary_data = summary_response.data if summary_response and summary_response.data else None
            
            return SessionWithMessages(
                **session_response.data,
                situation=Situation(**situation_response.data),
                messages=[DialogueMessage(**msg) for msg in messages_data],
                summary=SessionSummary(**summary_data) if summary_data else None
            )
        except Exception as e:
            print(f"Error getting session with messages: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def end_session(self, session_id: str) -> bool:
        """End a session and calculate duration"""
        try:
            # Get session start time
            session_response = self.supabase.table('roleplay_sessions').select('started_at').eq('id', session_id).maybe_single().execute()
            if not session_response or not session_response.data:
                print(f"Session {session_id} not found for ending")
                return False
            
            started_at_str = session_response.data['started_at']
            
            # Robust datetime parsing with fallback
            try:
                started_at = dateutil.parser.parse(started_at_str)
                if started_at.tzinfo is None:
                    started_at = started_at.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError) as parse_error:
                print(f"Warning: Could not parse started_at '{started_at_str}'. Error: {parse_error}")
                # Fallback: assume session started 10 minutes ago from now
                started_at = datetime.now(timezone.utc) - timedelta(minutes=10)

            # Use timezone-aware datetime for ended_at
            ended_at = datetime.now(timezone.utc)
            
            # Ensure positive duration
            duration_seconds = (ended_at - started_at).total_seconds()
            duration = max(1, int(abs(duration_seconds)))
            
            # Update session
            update_response = self.supabase.table('roleplay_sessions').update({
                'ended_at': ended_at.isoformat(),
                'status': 'completed',
                'session_duration': duration
            }).eq('id', session_id).execute()
            
            if update_response and update_response.data:
                print(f"Session {session_id} ended successfully. Duration: {duration} seconds")
                return True
            else:
                print(f"Failed to update session {session_id}")
                return False
            
        except Exception as e:
            print(f"Error ending session: {e}")
            import traceback
            traceback.print_exc()
            return False

class MessageService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def add_message(self, session_id: str, message_type: str, content: str) -> Optional[DialogueMessage]:
        """Add a new message to the session"""
        try:
            # Get current message count for ordering
            count_response = self.supabase.table('dialogue_messages').select('id', count='exact').eq('session_id', session_id).execute()
            message_order = count_response.count if count_response.count else 0
            
            message_data = {
                'session_id': session_id,
                'message_type': message_type,
                'content': content,
                'message_order': message_order,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
            response = self.supabase.table('dialogue_messages').insert(message_data).execute()
            if response.data:
                return DialogueMessage(**response.data[0])
            return None
        except Exception as e:
            print(f"Error adding message: {e}")
            return None
    
    async def get_session_messages(self, session_id: str) -> List[DialogueMessage]:
        """Get all messages for a session"""
        try:
            response = self.supabase.table('dialogue_messages').select('*').eq('session_id', session_id).order('message_order').execute()
            return [DialogueMessage(**msg) for msg in response.data]
        except Exception as e:
            print(f"Error getting session messages: {e}")
            return []

class AIPersonaService:
    """AI Persona Service with OpenAI GPT integration"""
    
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.openai_ready = True  # OpenAI integration is now active
        print("✅ OpenAI integration activated with GPT-4o-mini")
        
        # Detailed conversation starters by scenario
        self.conversation_starters = {
            'career': [
                "Hello! Thank you for coming in today. I'm excited to learn more about you and your background.",
                "Good morning! Please, have a seat. I'd love to start by hearing about your experience and what interests you about this role.",
                "Hi there! I appreciate you taking the time to meet with me today. Why don't we begin with you telling me a bit about yourself?"
            ],
            'customer_service': [
                "I can't believe this! I specifically bought this expensive laptop and now it's having issues!",
                "This is absolutely unacceptable! I paid good money for this product and now I want my money back!",
                "Listen, I've been a customer for years and this kind of quality is just not what I expect from your company!"
            ],
            'social': [
                "Hi! Thanks for meeting me here. This coffee shop has such a nice atmosphere, don't you think?",
                "It's so nice to finally meet in person! I have to say, this place makes an amazing latte.",
                "Hello! I hope you didn't have trouble finding this place. I love how cozy it is here."
            ],
            'management': [
                "Oh, hi... I wasn't expecting to talk today. Is everything okay?",
                "Hey, what's up? You mentioned you wanted to discuss something with me?",
                "Hi there. I hope this isn't about the project deadline... I've been working really hard on it."
            ],
            'networking': [
                "Hi! I don't think we've met yet. I'm Taylor from Creative Marketing Solutions. Great event tonight, isn't it?",
                "Hello there! I love meeting new people at these events. What brings you here tonight?",
                "Hi! I've been looking forward to this networking event all week. What kind of work do you do?"
            ]
        }
        
        # Enhanced response patterns for more realistic conversations
        self.response_patterns = {
            'career': {
                'questions': [
                    "That's impressive experience! Can you walk me through a specific project where you had to solve a challenging technical problem?",
                    "I see you have experience with {topic}. How would you handle a situation where you disagree with a team member's technical approach?",
                    "Tell me about a time when you had to learn a new technology quickly. What was your approach?",
                    "What interests you most about working at our company specifically?",
                    "How do you stay current with new developments in software engineering?",
                    "Describe a situation where you had to explain a complex technical concept to non-technical stakeholders."
                ],
                'follow_ups': [
                    "That's a great example. What was the most challenging part of that experience?",
                    "Interesting approach! How did you measure the success of that solution?",
                    "I can see you have strong problem-solving skills. What would you do differently if you faced a similar situation again?",
                    "That shows good initiative. How did your team react to your solution?"
                ]
            },
            'customer_service': {
                'escalations': [
                    "Well, that's something, but I still think I deserve compensation for all this trouble!",
                    "I appreciate that, but this has been going on for weeks now. What are you going to do to make this right?",
                    "Look, I understand you're trying to help, but I need a real solution here, not just apologies.",
                    "That's better, but I'm still not satisfied. Can you get your manager involved?"
                ],
                'de_escalations': [
                    "Okay, I appreciate you taking the time to explain that. What are my options here?",
                    "I can see you're trying to help. Let me think about what you've offered.",
                    "Thank you for being patient with me. I was just really frustrated about this situation.",
                    "That makes sense. I guess I was just expecting too much. What would you recommend?"
                ]
            },
            'social': {
                'interests': [
                    "That sounds really interesting! I've always wanted to try {topic}. How did you get started?",
                    "Oh wow, I love that too! Have you been to {related_place} recently?",
                    "That's so cool! I'm more of a {alternative_interest} person myself, but I can definitely appreciate {topic}.",
                    "I've heard great things about that! What's your favorite part about {topic}?"
                ],
                'questions': [
                    "So what do you like to do for fun when you're not working?",
                    "Have you seen any good movies lately? I'm always looking for recommendations.",
                    "This place has such good energy, don't you think? Do you come here often?",
                    "What's been the highlight of your week so far?"
                ]
            },
            'management': {
                'receptive': [
                    "Oh, I see what you mean. I hadn't thought about it that way before.",
                    "You're right, I can definitely work on that. Do you have any specific suggestions?",
                    "I appreciate the feedback. It's helpful to get your perspective on this.",
                    "That makes sense. I want to improve, so I'm glad you brought this up."
                ],
                'defensive': [
                    "I mean, I've been trying my best with everything that's on my plate right now...",
                    "I thought I was doing okay with that. Can you give me a specific example?",
                    "It's been really challenging lately with all the changes happening...",
                    "I guess I didn't realize it was coming across that way. That wasn't my intention."
                ]
            },
            'networking': {
                'professional': [
                    "That sounds like fascinating work! What's the most exciting project you're working on right now?",
                    "I'd love to hear more about your experience in {field}. We might have some interesting synergies.",
                    "Your background sounds really impressive. What got you interested in {topic} originally?",
                    "That's a great perspective! Have you noticed any emerging trends in your industry lately?"
                ],
                'collaborative': [
                    "You know, we might be able to help each other out. Would you be interested in connecting after the event?",
                    "That's exactly the kind of expertise our clients are looking for. Would you be open to a coffee meeting sometime?",
                    "I think there could be some real opportunities for collaboration between our companies.",
                    "This has been a great conversation! I'd love to continue it sometime. Do you have a business card?"
                ]
            }
        }
        
        self.response_templates = {
            'positive': [
                "That's really interesting! Tell me more about {topic}.",
                "I can see you have experience with {topic}. How did you develop those skills?",
                "That sounds like a great approach to {topic}. What results did you see?"
            ],
            'probing': [
                "Can you give me a specific example of {topic}?",
                "What was your biggest challenge when dealing with {topic}?",
                "How would you handle {topic} differently if you had to do it again?"
            ],
            'supportive': [
                "I understand your perspective on {topic}. Let's think about this together.",
                "That's a valid concern about {topic}. What if we tried a different approach?",
                "I appreciate you being open about {topic}. What support would help you most?"
            ]
        }
    
    async def generate_response(self, situation: Situation, conversation_history: List[DialogueMessage]) -> str:
        """Generate AI persona response - designed for easy OpenAI integration"""
        try:
            if self.openai_ready:
                return await self._generate_openai_response(situation, conversation_history)
            else:
                return await self._generate_mock_response(situation, conversation_history)
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I understand. Please continue."
    
    async def _generate_openai_response(self, situation: Situation, conversation_history: List[DialogueMessage]) -> str:
        """Generate authentic AI persona response using OpenAI GPT"""
        try:
            # Build conversation context with persona instructions
            messages = self._build_conversation_context(situation, conversation_history)
            
            # Call OpenAI API asynchronously
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=messages,
                    max_tokens=settings.OPENAI_MAX_TOKENS,
                    temperature=settings.OPENAI_TEMPERATURE,
                    presence_penalty=0.6,  # Encourage varied responses
                    frequency_penalty=0.3   # Reduce repetitive phrases
                )
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Validate and clean the response
            if not ai_response or len(ai_response) < 10:
                print(f"OpenAI response too short or empty: '{ai_response}', using fallback")
                return await self._generate_mock_response(situation, conversation_history)
            
            # Ensure response isn't too long for the UI
            if len(ai_response) > 500:
                ai_response = ai_response[:497] + "..."
            
            print(f"✅ Generated OpenAI response for {situation.category} scenario: {ai_response[:50]}...")
            return ai_response
            
        except openai.RateLimitError as e:
            print(f"OpenAI rate limit exceeded: {e}")
            return "I need a moment to think. Could you please rephrase that or try again in a moment?"
            
        except openai.APIError as e:
            print(f"OpenAI API error: {e}")
            return await self._generate_mock_response(situation, conversation_history)
            
        except Exception as e:
            print(f"Unexpected error with OpenAI: {e}")
            return await self._generate_mock_response(situation, conversation_history)
    
    async def _generate_mock_response(self, situation: Situation, conversation_history: List[DialogueMessage]) -> str:
        """Enhanced mock response generation"""
        # If this is the first message, use conversation starter
        if len(conversation_history) == 0:
            starters = self.conversation_starters.get(situation.category, 
                ["Hello! I'm ready to begin our roleplay session. How are you doing today?"])
            return random.choice(starters)
        
        # Get the last user message
        last_user_message = None
        for msg in reversed(conversation_history):
            if msg.message_type == 'user':
                last_user_message = msg.content
                break
        
        if not last_user_message:
            return "I'm listening. Please go ahead."
        
        # Generate contextual response based on situation and user input
        return self._generate_enhanced_contextual_response(situation, last_user_message, len(conversation_history))
    
    def _generate_enhanced_contextual_response(self, situation: Situation, user_message: str, message_count: int) -> str:
        """Enhanced contextual response generation with better conversation flow"""
        user_lower = user_message.lower()
        category = situation.category
        
        # Extract keywords and topics from user message
        topics = self._extract_topics(user_message)
        sentiment = self._analyze_sentiment(user_message)
        
        # Career/Interview scenarios
        if category == 'career':
            return self._generate_career_response(user_message, user_lower, message_count, topics, sentiment)
        
        # Customer Service scenarios
        elif category == 'customer_service':
            return self._generate_customer_service_response(user_message, user_lower, message_count, sentiment)
        
        # Social scenarios
        elif category == 'social':
            return self._generate_social_response(user_message, user_lower, message_count, topics)
        
        # Management scenarios
        elif category == 'management':
            return self._generate_management_response(user_message, user_lower, message_count, sentiment)
        
        # Networking scenarios
        elif category == 'networking':
            return self._generate_networking_response(user_message, user_lower, message_count, topics)
        
        # Default fallback
        return self._get_default_response(user_message, message_count)
    
    def _generate_career_response(self, user_message: str, user_lower: str, message_count: int, topics: list, sentiment: str) -> str:
        """Generate career/interview specific responses"""
        patterns = self.response_patterns.get('career', {})
        
        # Early conversation - establish rapport
        if message_count <= 2:
            return random.choice([
                "Great! Now, let me ask you - what interests you most about this position?",
                "Excellent background! What drew you to apply for this specific role?",
                "That's impressive. What would you say is your biggest professional accomplishment?"
            ])
        
        # Technical discussion
        if any(tech in user_lower for tech in ['python', 'javascript', 'code', 'programming', 'development', 'technical']):
            return random.choice([
                "Excellent! How do you approach debugging when you encounter a complex issue in your code?",
                "That's great experience. Can you walk me through your process for learning new technologies?",
                "I see you have strong technical skills. How do you balance code quality with delivery deadlines?"
            ])
        
        # Experience and background
        if any(word in user_lower for word in ['experience', 'background', 'worked', 'project']):
            return random.choice(patterns.get('questions', [
                "That's impressive experience. Can you give me a specific example of a challenging project you completed?"
            ]))
        
        # Teamwork and collaboration
        if any(word in user_lower for word in ['team', 'collaboration', 'colleagues', 'work with']):
            return random.choice([
                "Teamwork is crucial here. Tell me about a time when you had to resolve a conflict with a team member.",
                "Great! How do you handle situations where team members have different approaches to solving a problem?",
                "That shows good collaboration skills. What's your preferred communication style when working in teams?"
            ])
        
        # Follow-up questions
        return random.choice(patterns.get('follow_ups', [
            "That's a great example. What was the most challenging part of that experience?",
            "Interesting approach! How did you measure the success of that solution?",
            "I can see you have strong problem-solving skills. What would you do differently next time?"
        ]))
    
    def _generate_customer_service_response(self, user_message: str, user_lower: str, message_count: int, sentiment: str) -> str:
        """Generate customer service specific responses"""
        patterns = self.response_patterns.get('customer_service', {})
        
        # Positive sentiment - customer is calming down
        if sentiment == 'positive' or any(word in user_lower for word in ['understand', 'appreciate', 'thank', 'help']):
            return random.choice(patterns.get('de_escalations', [
                "Thank you for being patient with me. I was just really frustrated about this situation.",
                "I appreciate you taking the time to explain that. What are my options here?"
            ]))
        
        # Negative sentiment - customer is still upset
        elif any(word in user_lower for word in ['refund', 'money back', 'return']):
            return random.choice([
                "Finally! Yes, I want a full refund. I don't care about your 30-day policy - this is defective!",
                "That's what I've been asking for! How long will the refund process take?"
            ])
        
        # Manager escalation
        elif any(word in user_lower for word in ['manager', 'supervisor', 'boss']):
            return random.choice([
                "Yes, I think speaking to a manager would be appropriate. This situation needs to be escalated.",
                "Thank you, I would appreciate speaking with someone who has more authority to resolve this."
            ])
        
        # Default escalation responses
        return random.choice(patterns.get('escalations', [
            "Look, I understand you're trying to help, but I need a real solution here, not just apologies.",
            "I appreciate that, but this has been going on for weeks now. What are you going to do to make this right?"
        ]))
    
    def _generate_social_response(self, user_message: str, user_lower: str, message_count: int, topics: list) -> str:
        """Generate social conversation responses"""
        patterns = self.response_patterns.get('social', {})
        
        # Respond to interests and hobbies
        if any(word in user_lower for word in ['hobby', 'hobbies', 'interests', 'like to do', 'enjoy']):
            topic = topics[0] if topics else "that"
            return random.choice(patterns.get('interests', [])).replace('{topic}', topic).replace('{related_place}', 'the local area').replace('{alternative_interest}', 'reading')
        
        # Work and career discussion
        if any(word in user_lower for word in ['work', 'job', 'career', 'profession']):
            return random.choice([
                "That sounds like rewarding work! What's the most interesting part of your job?",
                "That's fascinating! How did you get started in that field?",
                "Work can be so demanding sometimes. How do you like to unwind after a busy day?"
            ])
        
        # Travel and experiences
        if any(word in user_lower for word in ['travel', 'vacation', 'trip', 'visit']):
            return random.choice([
                "Oh, I love traveling! What's your favorite place you've visited recently?",
                "That sounds amazing! I'm always looking for new travel ideas. Any recommendations?",
                "Travel is so enriching! Do you prefer adventure trips or more relaxing vacations?"
            ])
        
        # General conversation
        return random.choice(patterns.get('questions', [
            "So what do you like to do for fun when you're not working?",
            "This place has such good energy, don't you think? Do you come here often?",
            "What's been the highlight of your week so far?"
        ]))
    
    def _generate_management_response(self, user_message: str, user_lower: str, message_count: int, sentiment: str) -> str:
        """Generate management/feedback conversation responses"""
        patterns = self.response_patterns.get('management', {})
        
        # Positive/receptive responses
        if sentiment == 'positive' or any(word in user_lower for word in ['understand', 'appreciate', 'help', 'improve']):
            return random.choice(patterns.get('receptive', [
                "You're right, I can definitely work on that. Do you have any specific suggestions?",
                "I appreciate the feedback. It's helpful to get your perspective on this."
            ]))
        
        # Feedback and performance discussion
        elif any(word in user_lower for word in ['feedback', 'performance', 'improve', 'better']):
            return random.choice([
                "I really do want to get better. Maybe I just need some guidance on prioritizing tasks?",
                "That makes sense. I want to improve, so I'm glad you brought this up.",
                "I appreciate you taking the time to discuss this with me. How can I do better?"
            ])
        
        # Defensive but willing responses
        return random.choice(patterns.get('defensive', [
            "I thought I was doing okay with that. Can you give me a specific example?",
            "I guess I didn't realize it was coming across that way. That wasn't my intention."
        ]))
    
    def _generate_networking_response(self, user_message: str, user_lower: str, message_count: int, topics: list) -> str:
        """Generate networking conversation responses"""
        patterns = self.response_patterns.get('networking', {})
        
        # Business and professional topics
        if any(word in user_lower for word in ['business', 'company', 'work', 'industry', 'professional']):
            field = topics[0] if topics else "your field"
            return random.choice(patterns.get('professional', [])).replace('{field}', field).replace('{topic}', field)
        
        # Collaboration opportunities
        if any(word in user_lower for word in ['collaborate', 'partner', 'work together', 'opportunity']):
            return random.choice(patterns.get('collaborative', [
                "That's exactly the kind of expertise our clients are looking for. Would you be open to a coffee meeting sometime?",
                "I think there could be some real opportunities for collaboration between our companies."
            ]))
        
        # General networking
        return random.choice([
            "That sounds like fascinating work! What's the most exciting project you're working on right now?",
            "Your background sounds really impressive. What got you interested in this field originally?",
            "This has been a great conversation! What brings you to networking events like this?"
        ])
    
    def _extract_topics(self, message: str) -> list:
        """Extract key topics from user message"""
        # Simple keyword extraction - can be enhanced later
        tech_keywords = ['python', 'javascript', 'react', 'node', 'database', 'api', 'frontend', 'backend']
        business_keywords = ['marketing', 'sales', 'strategy', 'management', 'leadership', 'consulting']
        hobby_keywords = ['photography', 'hiking', 'reading', 'music', 'travel', 'sports', 'cooking']
        
        topics = []
        message_lower = message.lower()
        
        for keyword in tech_keywords + business_keywords + hobby_keywords:
            if keyword in message_lower:
                topics.append(keyword)
        
        return topics[:3]  # Return top 3 topics
    
    def _analyze_sentiment(self, message: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'love', 'like', 'appreciate', 'thank', 'understand', 'agree']
        negative_words = ['bad', 'terrible', 'hate', 'angry', 'frustrated', 'upset', 'problem', 'issue', 'complaint']
        
        message_lower = message.lower()
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _get_default_response(self, user_message: str, message_count: int) -> str:
        """Fallback responses for any scenario"""
        return random.choice([
            "That's really interesting. Can you tell me more about that?",
            "I see your point. How do you think we should move forward?",
            "That's a great perspective. What led you to that conclusion?",
            "I understand. What would you like to focus on next?",
            "That makes sense. How has that experience shaped your approach?",
            "Interesting! What's been your biggest learning from that?"
        ])
    
    def _build_conversation_context(self, situation: Situation, conversation_history: List[DialogueMessage]) -> list:
        """Build sophisticated conversation context for OpenAI with proper persona instructions"""
        
        # Create detailed system prompt based on scenario category
        system_prompt = self._create_system_prompt(situation)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history with proper role mapping
        for msg in conversation_history:
            role = "user" if msg.message_type == "user" else "assistant"
            messages.append({
                "role": role,
                "content": msg.content
            })
        
        return messages
    
    def _create_system_prompt(self, situation: Situation) -> str:
        """Create detailed system prompt for authentic persona responses"""
        
        base_instructions = f"""You are roleplaying in an interactive conversation training scenario. Here are your character details:

PERSONA SCRIPT: {situation.persona_script}

SCENARIO DETAILS:
- Title: {situation.title}  
- Description: {situation.description}
- Difficulty Level: {situation.difficulty_level}
- Category: {situation.category}

CRITICAL ROLEPLAY INSTRUCTIONS:
1. STAY IN CHARACTER at all times - you ARE this persona, not an AI assistant
2. Respond naturally as this character would in real life
3. Use the persona's speaking style, personality, and background
4. React authentically to what the user says
5. Keep responses conversational and realistic (50-150 words)
6. DO NOT break character or mention that you're roleplaying
7. DO NOT be overly helpful or AI-assistant-like"""

        # Add scenario-specific instructions
        if situation.category == 'career':
            base_instructions += """

CAREER SCENARIO INSTRUCTIONS:
- Ask follow-up questions about experience and skills
- Present realistic interview challenges
- Show genuine interest in candidate responses
- Maintain professional but approachable tone
- Ask behavioral and technical questions naturally"""

        elif situation.category == 'customer_service':
            base_instructions += """

CUSTOMER SERVICE SCENARIO INSTRUCTIONS:
- Express genuine frustration about the problem
- Vary your emotional state based on agent responses
- Be willing to escalate or de-escalate naturally
- Show appreciation when agent provides good solutions
- Remain human and realistic in your complaints"""

        elif situation.category == 'social':
            base_instructions += """

SOCIAL SCENARIO INSTRUCTIONS:
- Be genuinely interested in getting to know the person
- Share personal anecdotes and ask engaging questions
- Show enthusiasm about shared interests
- Maintain a friendly, warm conversational tone
- React naturally to awkward or smooth moments"""

        elif situation.category == 'management':
            base_instructions += """

MANAGEMENT SCENARIO INSTRUCTIONS:
- Show realistic employee emotions (nervousness, defensiveness, etc.)
- Be receptive to constructive feedback when delivered well
- Express concerns and ask clarifying questions
- Demonstrate willingness to improve when supported properly
- React authentically to different management approaches"""

        elif situation.category == 'networking':
            base_instructions += """

NETWORKING SCENARIO INSTRUCTIONS:
- Show genuine professional interest in others
- Share relevant business experiences and insights
- Look for collaboration opportunities naturally
- Maintain professional enthusiasm
- Exchange ideas and explore mutual benefits"""

        base_instructions += """

RESPONSE GUIDELINES:
- Keep responses between 20-150 words
- Use natural speech patterns with contractions
- Include realistic hesitations, expressions, and emotions
- Ask engaging follow-up questions when appropriate
- Match the energy and tone of the conversation
- Avoid being overly formal unless the character demands it"""

        return base_instructions

class FeedbackService:
    """Service for generating enhanced session feedback using OpenAI"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_session_feedback(self, session_id: str) -> Optional[SessionSummary]:
        """Generate comprehensive AI-powered feedback for a completed session"""
        try:
            # Get session with messages
            session_service = SessionService()
            session_data = await session_service.get_session_with_messages(session_id)
            
            if not session_data or not session_data.messages:
                print(f"No session data or messages found for session {session_id}")
                return None
            
            # Generate enhanced feedback using OpenAI
            try:
                feedback = await self._generate_ai_feedback(session_data)
                print(f"✅ Generated AI feedback for session {session_id}")
            except Exception as ai_error:
                print(f"AI feedback generation failed, using traditional analysis: {ai_error}")
                feedback = self._analyze_conversation(session_data)
            
            # Save feedback to database
            feedback_data = {
                'session_id': session_id,
                'performance_score': feedback['score'],
                'feedback_text': feedback['overview'],
                'strengths': feedback['strengths'],
                'improvement_areas': feedback['improvements'],
                'key_insights': feedback['insights']
            }
            
            response = self.supabase.table('session_summaries').insert(feedback_data).execute()
            if response and response.data and len(response.data) > 0:
                return SessionSummary(**response.data[0])
            
            print(f"Failed to save feedback to database for session {session_id}")
            return None
            
        except Exception as e:
            print(f"Error generating feedback: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _generate_ai_feedback(self, session_data: SessionWithMessages) -> Dict[str, Any]:
        """Generate sophisticated feedback using OpenAI analysis"""
        
        # Build conversation transcript for analysis
        transcript = self._build_transcript(session_data)
        
        # Create feedback analysis prompt
        feedback_prompt = f"""You are an expert communication coach analyzing a roleplay conversation.

ROLEPLAY SCENARIO:
- Title: {session_data.situation.title}
- Category: {session_data.situation.category} 
- Description: {session_data.situation.description}

FULL CONVERSATION TRANSCRIPT:
{transcript}

Analyze the USER's communication performance specifically for this {session_data.situation.category} scenario.
Focus on engagement level, communication style, and effectiveness.

Please provide a comprehensive analysis in the following format:

PERFORMANCE SCORE: [Give a score from 60-95 based on communication effectiveness]

OVERVIEW: [2-3 sentences summarizing overall performance]

STRENGTHS: [List 2-3 specific strengths demonstrated, separated by ' • ']

IMPROVEMENT AREAS: [List 2-3 specific actionable improvements, separated by ' • ']

KEY INSIGHTS: [2-3 key learning points for future development, separated by ' • ']

Focus on practical, actionable feedback that helps improve communication skills. Be constructive but direct - this is for skill development."""

        # Call OpenAI for feedback analysis
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": feedback_prompt}],
                max_tokens=400,
                temperature=0.3  # Lower temperature for more consistent feedback
            )
        )
        
        feedback_text = response.choices[0].message.content.strip()
        
        # Parse the structured feedback
        return self._parse_ai_feedback(feedback_text, session_data)
    
    def _build_transcript(self, session_data: SessionWithMessages) -> str:
        """Build a clean conversation transcript for analysis"""
        transcript_lines = []
        
        transcript_lines.append(f"=== ROLEPLAY CONVERSATION ({len(session_data.messages)} messages) ===")
        transcript_lines.append(f"Scenario: {session_data.situation.title}")
        
        for i, msg in enumerate(session_data.messages, 1):
            speaker = "USER" if msg.message_type == "user" else "AI PERSONA"
            timestamp = msg.timestamp.strftime('%H:%M:%S')
            transcript_lines.append(f"[{timestamp}] {speaker}: {msg.content}")
        
        return "\n".join(transcript_lines)
    
    def _parse_ai_feedback(self, feedback_text: str, session_data: SessionWithMessages) -> Dict[str, Any]:
        """Parse structured feedback from OpenAI response"""
        try:
            # Extract components using simple parsing
            lines = feedback_text.split('\n')
            
            score = 75  # Default score
            overview = ""
            strengths = ""
            improvements = ""
            insights = ""
            
            current_section = ""
            content_buffer = []
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("PERFORMANCE SCORE:"):
                    score_text = line.replace("PERFORMANCE SCORE:", "").strip()
                    # Extract number from score text
                    import re
                    score_match = re.search(r'\d+', score_text)
                    if score_match:
                        score = min(95, max(60, int(score_match.group())))
                    
                elif line.startswith("OVERVIEW:"):
                    current_section = "overview"
                    overview = line.replace("OVERVIEW:", "").strip()
                    
                elif line.startswith("STRENGTHS:"):
                    current_section = "strengths"
                    strengths = line.replace("STRENGTHS:", "").strip()
                    
                elif line.startswith("IMPROVEMENT AREAS:"):
                    current_section = "improvements"
                    improvements = line.replace("IMPROVEMENT AREAS:", "").strip()
                    
                elif line.startswith("KEY INSIGHTS:"):
                    current_section = "insights"
                    insights = line.replace("KEY INSIGHTS:", "").strip()
                    
                elif line and current_section:
                    # Continue building content for current section
                    if current_section == "overview" and line:
                        overview = (overview + " " + line).strip()
                    elif current_section == "strengths" and line:
                        strengths = (strengths + " " + line).strip()
                    elif current_section == "improvements" and line:
                        improvements = (improvements + " " + line).strip()
                    elif current_section == "insights" and line:
                        insights = (insights + " " + line).strip()
            
            # Fallback to basic analysis if parsing fails
            if not overview:
                overview = f"Your {session_data.situation.category} conversation demonstrated good engagement with room for improvement in specific areas."
            
            if not strengths:
                user_messages = [msg for msg in session_data.messages if msg.message_type == 'user']
                avg_length = sum(len(msg.content.split()) for msg in user_messages) / max(len(user_messages), 1)
                strengths = f"Maintained consistent communication throughout the session • Average response length of {avg_length:.0f} words shows good detail"
            
            if not improvements:
                improvements = f"Practice more specific examples when discussing experience • Work on asking clarifying questions • Focus on demonstrating {session_data.situation.category} skills more clearly"
            
            if not insights:
                insights = f"{session_data.situation.category.title()} scenarios require authentic communication • Building rapport is essential for successful interactions • Practice makes perfect"
            
            return {
                'score': score,
                'overview': overview,
                'strengths': strengths,
                'improvements': improvements,
                'insights': insights
            }
            
        except Exception as e:
            print(f"Error parsing AI feedback: {e}")
            # Fallback to traditional analysis
            return self._analyze_conversation(session_data)
    
    def _analyze_conversation(self, session_data: SessionWithMessages) -> Dict[str, Any]:
        """Analyze conversation and generate feedback"""
        user_messages = [msg for msg in session_data.messages if msg.message_type == 'user']
        total_messages = len(user_messages)
        
        # Calculate basic metrics
        avg_message_length = sum(len(msg.content.split()) for msg in user_messages) / max(total_messages, 1)
        
        # Determine performance score based on engagement and message quality
        score = min(85, max(60, int(70 + (total_messages * 2) + (avg_message_length * 0.5))))
        
        # Generate category-specific feedback
        category = session_data.situation.category
        situation_title = session_data.situation.title
        
        feedback = {
            'score': score,
            'overview': self._generate_overview_feedback(category, total_messages, avg_message_length),
            'strengths': self._generate_strengths_feedback(category, user_messages),
            'improvements': self._generate_improvement_feedback(category, user_messages),
            'insights': self._generate_insights_feedback(category, situation_title, total_messages)
        }
        
        return feedback
    
    def _generate_overview_feedback(self, category: str, message_count: int, avg_length: float) -> str:
        """Generate overall feedback summary"""
        engagement_level = "high" if message_count >= 8 else "moderate" if message_count >= 5 else "low"
        detail_level = "detailed" if avg_length >= 15 else "adequate" if avg_length >= 8 else "brief"
        
        feedback_templates = {
            'career': f"Your interview performance showed {engagement_level} engagement with {detail_level} responses. You demonstrated good communication skills and showed interest in the role.",
            'customer_service': f"You handled this challenging customer service scenario with {engagement_level} engagement. Your responses were {detail_level} and showed professional communication skills.",
            'social': f"Your conversation skills demonstrated {engagement_level} social engagement with {detail_level} responses. You showed good interpersonal communication abilities.",
            'management': f"Your approach to receiving feedback showed {engagement_level} engagement and {detail_level} responses. You demonstrated openness to improvement.",
            'networking': f"Your networking conversation showed {engagement_level} engagement with {detail_level} responses. You demonstrated good professional communication skills."
        }
        
        return feedback_templates.get(category, f"You showed {engagement_level} engagement in this roleplay scenario with {detail_level} responses.")
    
    def _generate_strengths_feedback(self, category: str, user_messages: List[DialogueMessage]) -> str:
        """Generate strengths feedback based on message analysis"""
        message_texts = [msg.content.lower() for msg in user_messages]
        
        strengths = []
        
        # Check for positive communication patterns
        if any('thank' in text for text in message_texts):
            strengths.append("Good use of polite expressions and gratitude")
        
        if any(len(text.split()) > 20 for text in message_texts):
            strengths.append("Ability to provide detailed explanations when needed")
        
        if any('?' in text for text in message_texts):
            strengths.append("Good questioning skills and curiosity")
        
        # Category-specific strengths
        if category == 'career':
            if any('experience' in text or 'project' in text for text in message_texts):
                strengths.append("Effectively highlighted relevant experience")
            if any('team' in text or 'collaboration' in text for text in message_texts):
                strengths.append("Demonstrated understanding of teamwork importance")
        
        elif category == 'customer_service':
            if any('understand' in text or 'help' in text for text in message_texts):
                strengths.append("Showed empathy and willingness to help")
            if any('solution' in text or 'resolve' in text for text in message_texts):
                strengths.append("Focused on problem-solving approaches")
        
        return " • ".join(strengths) if strengths else "Maintained consistent communication throughout the session"
    
    def _generate_improvement_feedback(self, category: str, user_messages: List[DialogueMessage]) -> str:
        """Generate improvement suggestions"""
        improvements = []
        
        if len(user_messages) < 5:
            improvements.append("Try to engage more deeply by asking follow-up questions")
        
        avg_length = sum(len(msg.content.split()) for msg in user_messages) / max(len(user_messages), 1)
        if avg_length < 10:
            improvements.append("Provide more detailed responses to show depth of thinking")
        
        # Category-specific improvements
        if category == 'career':
            improvements.append("Consider using the STAR method (Situation, Task, Action, Result) for behavioral questions")
            improvements.append("Research more specific details about the company and role")
        
        elif category == 'customer_service':
            improvements.append("Practice acknowledging customer emotions before presenting solutions")
            improvements.append("Develop a repertoire of service recovery options")
        
        elif category == 'social':
            improvements.append("Practice sharing personal anecdotes to build connection")
            improvements.append("Ask more open-ended questions to keep conversations flowing")
        
        elif category == 'management':
            improvements.append("Practice active listening techniques and paraphrasing")
            improvements.append("Focus on collaborative problem-solving approaches")
        
        elif category == 'networking':
            improvements.append("Prepare elevator pitches about yourself and your work")
            improvements.append("Practice transitioning conversations toward mutual opportunities")
        
        return " • ".join(improvements) if improvements else "Continue practicing to build confidence and fluency"
    
    def _generate_insights_feedback(self, category: str, situation_title: str, message_count: int) -> str:
        """Generate key insights and learning points"""
        insights = []
        
        if message_count >= 8:
            insights.append("You showed good stamina for extended conversations")
        
        # Category-specific insights
        category_insights = {
            'career': "Job interviews are about demonstrating fit - both your qualifications and cultural alignment with the organization.",
            'customer_service': "Effective customer service balances empathy with practical solutions, turning negative experiences into positive outcomes.",
            'social': "Great conversations happen when both people feel heard and valued - focus on genuine curiosity about others.",
            'management': "Giving and receiving feedback effectively requires trust, specificity, and a focus on growth rather than criticism.",
            'networking': "Successful networking is about building genuine relationships, not just exchanging business cards."
        }
        
        insights.append(category_insights.get(category, "Effective communication requires practice, patience, and genuine interest in others."))
        insights.append("Consider recording yourself practicing to identify speech patterns and areas for improvement.")
        
        return " • ".join(insights)