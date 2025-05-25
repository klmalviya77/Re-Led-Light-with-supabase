import os
from supabase import create_client, Client
import logging

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    try:
        supabase: Client = create_client(url, key)
        logging.info("Supabase client initialized successfully")
        return supabase
    except Exception as e:
        logging.error(f"Failed to initialize Supabase client: {e}")
        raise

# Initialize the client
supabase = get_supabase_client()