"""
Database configuration module for the Note Taking App.
Handles database connection string configuration for different environments.
"""
import os

def get_database_uri():
    """
    Returns the appropriate database URI based on the environment.
    
    Priority:
    1. DATABASE_URL environment variable (for Supabase or other external DB)
    2. Vercel environment - uses in-memory SQLite
    3. Local development - uses local SQLite file
    
    Returns:
        str: Database connection URI
    """
    # Check for external database URL (e.g., Supabase PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Handle Supabase connection string format
        # Supabase might provide postgres:// which SQLAlchemy 1.4+ requires postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # Vercel deployment without external database - use in-memory
    if os.environ.get('VERCEL'):
        return 'sqlite:///:memory:'
    
    # Local development - use local SQLite file
    root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(root_dir, 'database', 'app.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return f"sqlite:///{db_path}"

def get_database_config():
    """
    Returns a dictionary of database configuration settings.
    
    Returns:
        dict: Configuration dictionary for Flask app
    """
    return {
        'SQLALCHEMY_DATABASE_URI': get_database_uri(),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,  # Verify connections before using
            'pool_recycle': 300,    # Recycle connections after 5 minutes
        }
    }
