from supabase import create_client, Client
from config import settings

# Use Supabase client for all database operations
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

def get_supabase_client():
    """Get Supabase client for database operations"""
    return supabase

def init_db():
    """Initialize database connection"""
    try:
        # Test the connection
        response = supabase.table('situations').select('count', count='exact').limit(1).execute()
        print(f"Database connection successful. Situations table has {response.count} records.")
    except Exception as e:
        print(f"Database connection warning: {e}")
        print("Proceeding with Supabase client for database operations")

def get_db():
    """Dependency for getting database session"""
    return get_supabase_client()