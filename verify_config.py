"""
Configuration verification script.
Checks if the environment is properly configured for database connection.
"""
import os
import sys

def check_env_file():
    """Check if .env file exists"""
    print("1. Checking for .env file...")
    if os.path.exists('.env'):
        print("   ✅ .env file found")
        return True
    else:
        print("   ⚠️  .env file not found")
        print("   → Run: cp .env.example .env")
        return False

def check_database_url():
    """Check if DATABASE_URL is configured"""
    print("\n2. Checking DATABASE_URL...")
    
    # Try to load from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("   ⚠️  python-dotenv not installed")
        print("   → Run: pip install python-dotenv")
        return False
    
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("   ℹ️  DATABASE_URL not set (will use local SQLite)")
        print("   → For Supabase: Set DATABASE_URL in .env file")
        return None
    
    # Check if it's PostgreSQL
    if 'postgresql://' in database_url or 'postgres://' in database_url:
        # Mask password
        parts = database_url.split('@')
        if len(parts) > 1:
            masked = parts[0].split(':')[0] + ':***@' + parts[1]
        else:
            masked = database_url
        print(f"   ✅ DATABASE_URL configured (PostgreSQL)")
        print(f"   → {masked}")
        return True
    else:
        print(f"   ⚠️  DATABASE_URL is set but not PostgreSQL: {database_url[:50]}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n3. Checking Python packages...")
    
    required_packages = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'psycopg2': 'psycopg2-binary',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"   ✅ {package_name} installed")
        except ImportError:
            print(f"   ❌ {package_name} NOT installed")
            missing.append(package_name)
    
    if missing:
        print(f"\n   → Run: pip install {' '.join(missing)}")
        return False
    
    return True

def check_database_connection():
    """Check if database connection works"""
    print("\n4. Checking database connection...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from src.main import app, db
        
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
            
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'postgresql' in db_uri:
                print("   ✅ Successfully connected to PostgreSQL")
            elif 'sqlite' in db_uri:
                print("   ✅ Successfully connected to SQLite")
            else:
                print(f"   ✅ Successfully connected to database")
            
            return True
    except Exception as e:
        print(f"   ❌ Database connection failed: {str(e)}")
        return False

def check_gitignore():
    """Check if .env is in .gitignore"""
    print("\n5. Checking .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("   ⚠️  .gitignore not found")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    if '.env' in content:
        print("   ✅ .env is in .gitignore (safe from git)")
        return True
    else:
        print("   ⚠️  .env is NOT in .gitignore")
        print("   → Add '.env' to .gitignore file")
        return False

def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("  CONFIGURATION VERIFICATION")
    print("=" * 60)
    print()
    
    results = []
    
    # Run checks
    results.append(("Environment file", check_env_file()))
    results.append(("Python packages", check_python_packages()))
    results.append(("Database URL", check_database_url()))
    results.append(("Git ignore", check_gitignore()))
    results.append(("Database connection", check_database_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("  VERIFICATION SUMMARY")
    print("=" * 60)
    
    for check_name, result in results:
        if result is True:
            print(f"✅ {check_name}: PASSED")
        elif result is False:
            print(f"❌ {check_name}: FAILED")
        else:
            print(f"ℹ️  {check_name}: INFO")
    
    # Count results
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    
    print(f"\n{passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 Configuration is ready!")
        print("\nNext steps:")
        print("1. If using Supabase, configure DATABASE_URL in .env")
        print("2. Run: python test_supabase.py")
        print("3. Run: python src/main.py")
    else:
        print("\n⚠️  Please fix the issues above before proceeding")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
