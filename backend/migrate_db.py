"""
Database Migration Script for Intake Request System
Run this script to add the new tables to an existing database.

Usage:
    python migrate_db.py

Make sure your DATABASE_URL is set in .env file or environment variables.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_database():
    """Create new tables and insert default states"""
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL in your .env file or environment")
        return False
    
    print(f"🔌 Connecting to database...")
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("✅ Connected successfully")
            
            # Create request_states table
            print("\n📋 Creating request_states table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS request_states (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL UNIQUE,
                    description VARCHAR,
                    color VARCHAR,
                    is_active BOOLEAN DEFAULT TRUE,
                    display_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ request_states table created")
            
            # Create intake_requests table
            print("\n📋 Creating intake_requests table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS intake_requests (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    description TEXT,
                    functional_area VARCHAR NOT NULL,
                    submitter_name VARCHAR NOT NULL,
                    submitter_email VARCHAR NOT NULL,
                    has_it_partner BOOLEAN NOT NULL,
                    it_partner_name VARCHAR,
                    it_partner_email VARCHAR,
                    selected_help_types TEXT NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ intake_requests table created")
            
            # Create request_state_assignments table
            print("\n📋 Creating request_state_assignments table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS request_state_assignments (
                    id SERIAL PRIMARY KEY,
                    request_id INTEGER NOT NULL REFERENCES intake_requests(id) ON DELETE CASCADE,
                    state_id INTEGER NOT NULL REFERENCES request_states(id) ON DELETE CASCADE,
                    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assigned_by VARCHAR,
                    notes TEXT,
                    UNIQUE(request_id, state_id)
                )
            """))
            conn.commit()
            print("✅ request_state_assignments table created")
            
            # Check if default states already exist
            print("\n🔍 Checking for existing states...")
            result = conn.execute(text("SELECT COUNT(*) FROM request_states"))
            count = result.scalar()
            
            if count and count > 0:
                print(f"ℹ️  Found {count} existing states, skipping default state insertion")
            else:
                # Insert default request states
                print("\n📝 Inserting default request states...")
                conn.execute(text("""
                    INSERT INTO request_states (name, description, color, display_order) VALUES
                        ('New', 'Request has been submitted and is awaiting review', '#3b82f6', 1),
                        ('In Review', 'Request is being reviewed by the team', '#8b5cf6', 2),
                        ('Assigned', 'Request has been assigned to a team member', '#0ea5e9', 3),
                        ('In Progress', 'Work on the request has started', '#f59e0b', 4),
                        ('Blocked', 'Request is blocked and cannot proceed', '#ef4444', 5),
                        ('Completed', 'Request has been successfully completed', '#10b981', 6),
                        ('Rejected', 'Request has been rejected', '#6b7280', 7)
                """))
                conn.commit()
                print("✅ Default states inserted")
            
            print("\n🎉 Migration completed successfully!")
            print("\nNew tables created:")
            print("  - request_states")
            print("  - intake_requests")
            print("  - request_state_assignments")
            
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: Migration failed")
        print(f"Error details: {str(e)}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration for Intake Request System")
    print("=" * 60)
    
    success = migrate_database()
    
    if success:
        print("\n✅ All done! Your database is ready.")
        print("\nNext steps:")
        print("  1. Start your backend server: uvicorn main:app --reload")
        print("  2. Test the new features in the UI")
    else:
        print("\n❌ Migration failed. Please check the error above.")
        exit(1)
