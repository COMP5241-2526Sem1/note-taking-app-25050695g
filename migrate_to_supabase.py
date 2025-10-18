"""
Migration script to transfer data from local SQLite to Supabase PostgreSQL.
Use this script if you have existing data in the local database that you want to migrate.
"""
import os
import sys
import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from src.main import app, db
from src.models.note import Note
from src.models.user import User

# Load environment variables
load_dotenv()

def check_sqlite_exists():
    """Check if local SQLite database exists"""
    root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(root_dir, 'database', 'app.db')
    return os.path.exists(db_path), db_path

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Check if DATABASE_URL is set
    if not os.environ.get('DATABASE_URL'):
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("   Please set DATABASE_URL in your .env file")
        return False
    
    # Check if PostgreSQL
    db_url = os.environ.get('DATABASE_URL')
    if 'postgresql' not in db_url and 'postgres' not in db_url:
        print("❌ ERROR: DATABASE_URL does not point to a PostgreSQL database")
        print(f"   Current DATABASE_URL: {db_url}")
        return False
    
    # Check if SQLite exists
    sqlite_exists, sqlite_path = check_sqlite_exists()
    if not sqlite_exists:
        print("❌ ERROR: Local SQLite database not found")
        print(f"   Expected location: {sqlite_path}")
        return False
    
    print("\n" + "=" * 60)
    print("  DATABASE MIGRATION: SQLite → PostgreSQL")
    print("=" * 60)
    print(f"\nSource: {sqlite_path}")
    print(f"Target: {db_url[:50]}...")
    
    # Connect to SQLite
    try:
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        cursor = sqlite_conn.cursor()
        print("\n✅ Connected to SQLite database")
    except Exception as e:
        print(f"\n❌ Failed to connect to SQLite: {str(e)}")
        return False
    
    with app.app_context():
        try:
            # Check PostgreSQL connection
            db.session.execute(db.text('SELECT 1'))
            print("✅ Connected to PostgreSQL database")
            
            # Count existing records
            existing_users = User.query.count()
            existing_notes = Note.query.count()
            
            if existing_users > 0 or existing_notes > 0:
                print(f"\n⚠️  WARNING: Target database already contains data:")
                print(f"   Users: {existing_users}")
                print(f"   Notes: {existing_notes}")
                response = input("\nDo you want to continue? This will add to existing data. (yes/no): ")
                if response.lower() != 'yes':
                    print("Migration cancelled")
                    return False
            
            # Migrate Users
            print("\n" + "-" * 60)
            print("Migrating Users...")
            print("-" * 60)
            
            try:
                cursor.execute("SELECT * FROM user")
                users = cursor.fetchall()
                
                if not users:
                    print("No users found in SQLite database")
                else:
                    migrated_users = 0
                    for row in users:
                        # Check if user already exists
                        existing = User.query.filter_by(username=row['username']).first()
                        if existing:
                            print(f"⚠️  User '{row['username']}' already exists, skipping...")
                            continue
                        
                        user = User(
                            username=row['username'],
                            email=row['email']
                        )
                        db.session.add(user)
                        migrated_users += 1
                        print(f"   ✅ Migrated user: {row['username']}")
                    
                    if migrated_users > 0:
                        db.session.commit()
                        print(f"\n✅ Successfully migrated {migrated_users} user(s)")
                    else:
                        print(f"\nℹ️  No new users to migrate")
            except sqlite3.OperationalError:
                print("ℹ️  User table not found in SQLite database")
            
            # Migrate Notes
            print("\n" + "-" * 60)
            print("Migrating Notes...")
            print("-" * 60)
            
            try:
                cursor.execute("SELECT * FROM note")
                notes = cursor.fetchall()
                
                if not notes:
                    print("No notes found in SQLite database")
                else:
                    migrated_notes = 0
                    for row in notes:
                        note = Note(
                            title=row['title'],
                            content=row['content'],
                            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow(),
                            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else datetime.utcnow()
                        )
                        db.session.add(note)
                        migrated_notes += 1
                        print(f"   ✅ Migrated note: {row['title'][:50]}...")
                    
                    if migrated_notes > 0:
                        db.session.commit()
                        print(f"\n✅ Successfully migrated {migrated_notes} note(s)")
                    else:
                        print(f"\nℹ️  No notes to migrate")
            except sqlite3.OperationalError:
                print("ℹ️  Note table not found in SQLite database")
            
            # Summary
            print("\n" + "=" * 60)
            print("  MIGRATION SUMMARY")
            print("=" * 60)
            
            final_users = User.query.count()
            final_notes = Note.query.count()
            
            print(f"\nFinal counts in PostgreSQL:")
            print(f"   Users: {final_users}")
            print(f"   Notes: {final_notes}")
            print("\n🎉 Migration completed successfully!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            db.session.rollback()
            return False
        finally:
            sqlite_conn.close()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  SQLite to PostgreSQL Migration Tool")
    print("=" * 60)
    print("\nThis script will migrate data from your local SQLite database")
    print("to your Supabase PostgreSQL database.")
    print("\nPrerequisites:")
    print("1. DATABASE_URL must be set in .env file")
    print("2. Local SQLite database must exist (database/app.db)")
    print("\n")
    
    response = input("Do you want to proceed with migration? (yes/no): ")
    
    if response.lower() != 'yes':
        print("\nMigration cancelled.")
        sys.exit(0)
    
    success = migrate_data()
    sys.exit(0 if success else 1)
