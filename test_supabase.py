"""
Test script for Supabase PostgreSQL database integration.
This script tests database connectivity and CRUD operations.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from src.main import app, db
from src.models.note import Note
from src.models.user import User
from datetime import datetime

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_database_connection():
    """Test basic database connection"""
    print_section("Testing Database Connection")
    
    with app.app_context():
        try:
            # Try to execute a simple query
            db.session.execute(db.text('SELECT 1'))
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            
            # Mask password in output
            if 'postgresql://' in db_uri:
                parts = db_uri.split('@')
                if len(parts) > 1:
                    masked_uri = parts[0].split(':')[0] + ':***@' + parts[1]
                else:
                    masked_uri = db_uri
            else:
                masked_uri = db_uri
            
            print(f"✅ Successfully connected to database")
            print(f"   Database URI: {masked_uri}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to database: {str(e)}")
            return False

def test_create_tables():
    """Test table creation"""
    print_section("Testing Table Creation")
    
    with app.app_context():
        try:
            # Drop all tables and recreate
            db.drop_all()
            db.create_all()
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Tables created successfully:")
            for table in tables:
                print(f"   - {table}")
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {str(e)}")
            return False

def test_user_crud():
    """Test User CRUD operations"""
    print_section("Testing User CRUD Operations")
    
    with app.app_context():
        try:
            # Create
            print("\n1. CREATE - Creating test user...")
            user = User(username="testuser", email="test@example.com")
            db.session.add(user)
            db.session.commit()
            print(f"   ✅ Created user: {user.to_dict()}")
            user_id = user.id
            
            # Read
            print("\n2. READ - Reading user...")
            user = User.query.get(user_id)
            print(f"   ✅ Retrieved user: {user.to_dict()}")
            
            # Update
            print("\n3. UPDATE - Updating user email...")
            user.email = "updated@example.com"
            db.session.commit()
            print(f"   ✅ Updated user: {user.to_dict()}")
            
            # Delete
            print("\n4. DELETE - Deleting user...")
            db.session.delete(user)
            db.session.commit()
            print(f"   ✅ User deleted successfully")
            
            # Verify deletion
            user = User.query.get(user_id)
            if user is None:
                print(f"   ✅ Verified user is deleted")
            else:
                print(f"   ❌ User still exists after deletion")
                return False
            
            return True
        except Exception as e:
            print(f"❌ User CRUD test failed: {str(e)}")
            db.session.rollback()
            return False

def test_note_crud():
    """Test Note CRUD operations"""
    print_section("Testing Note CRUD Operations")
    
    with app.app_context():
        try:
            # Create
            print("\n1. CREATE - Creating test note...")
            note = Note(title="Test Note", content="This is a test note content")
            db.session.add(note)
            db.session.commit()
            print(f"   ✅ Created note: {note.to_dict()}")
            note_id = note.id
            
            # Read
            print("\n2. READ - Reading note...")
            note = Note.query.get(note_id)
            print(f"   ✅ Retrieved note: {note.to_dict()}")
            
            # Update
            print("\n3. UPDATE - Updating note...")
            note.title = "Updated Test Note"
            note.content = "This content has been updated"
            db.session.commit()
            print(f"   ✅ Updated note: {note.to_dict()}")
            
            # List all notes
            print("\n4. LIST - Getting all notes...")
            notes = Note.query.order_by(Note.updated_at.desc()).all()
            print(f"   ✅ Found {len(notes)} note(s)")
            for n in notes:
                print(f"      - {n.title}")
            
            # Delete
            print("\n5. DELETE - Deleting note...")
            db.session.delete(note)
            db.session.commit()
            print(f"   ✅ Note deleted successfully")
            
            # Verify deletion
            note = Note.query.get(note_id)
            if note is None:
                print(f"   ✅ Verified note is deleted")
            else:
                print(f"   ❌ Note still exists after deletion")
                return False
            
            return True
        except Exception as e:
            print(f"❌ Note CRUD test failed: {str(e)}")
            db.session.rollback()
            return False

def test_multiple_notes():
    """Test creating and managing multiple notes"""
    print_section("Testing Multiple Notes")
    
    with app.app_context():
        try:
            print("\nCreating 5 test notes...")
            for i in range(5):
                note = Note(
                    title=f"Note {i+1}",
                    content=f"Content for note {i+1}"
                )
                db.session.add(note)
            db.session.commit()
            print(f"   ✅ Created 5 notes")
            
            # Query all notes
            notes = Note.query.all()
            print(f"\nQuerying all notes...")
            print(f"   ✅ Found {len(notes)} notes")
            
            # Search notes
            print(f"\nSearching for 'Note 3'...")
            results = Note.query.filter(Note.title.contains('Note 3')).all()
            print(f"   ✅ Found {len(results)} matching notes")
            
            # Clean up
            print(f"\nCleaning up test notes...")
            Note.query.delete()
            db.session.commit()
            print(f"   ✅ All test notes deleted")
            
            return True
        except Exception as e:
            print(f"❌ Multiple notes test failed: {str(e)}")
            db.session.rollback()
            return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  SUPABASE POSTGRESQL DATABASE TESTS")
    print("=" * 60)
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("\n⚠️  WARNING: No DATABASE_URL found in environment")
        print("   Tests will run with local SQLite database")
    elif 'postgresql://' in database_url or 'postgres://' in database_url:
        print("\n✅ Using PostgreSQL database (Supabase)")
    
    results = []
    
    # Run tests
    results.append(("Database Connection", test_database_connection()))
    results.append(("Table Creation", test_create_tables()))
    results.append(("User CRUD Operations", test_user_crud()))
    results.append(("Note CRUD Operations", test_note_crud()))
    results.append(("Multiple Notes", test_multiple_notes()))
    
    # Print summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Database is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
