#!/usr/bin/env python3
"""
Database migration script for IT Platform CRM

ALWAYS drops and recreates all tables from scratch to ensure correct schema.
This guarantees all columns match models.py exactly.

Usage:
    python migrate_db.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def migrate_database():
    """Drop and recreate all database tables from scratch"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("\nPlease set DATABASE_URL in your .env file or environment")
        print("Example: DATABASE_URL=postgresql://user:pass@host:5432/dbname")
        return False
    
    print("=" * 60)
    print("Database Migration - IT Platform CRM")
    print("=" * 60)
    print("\n🚀 Starting database migration...")
    print(f"📍 Connecting to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
    print("\n⚠️  This will DROP and RECREATE all tables!")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Drop all tables in reverse dependency order
            print("\n🗑️  Dropping existing tables...")
            tables_to_drop = [
                "request_state_assignments",
                "intake_requests", 
                "request_states",
                "primary_it_partners",
                "platforms_crm",
                "updates",
                "use_cases",
                "accounts"
            ]
            for table in tables_to_drop:
                conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            conn.commit()
            print("✅ All tables dropped")
            
            # Create accounts table with ALL columns from models.py
            print("\n📋 Creating accounts table...")
            conn.execute(text("""
                CREATE TABLE accounts (
                    uid VARCHAR PRIMARY KEY,
                    team VARCHAR,
                    business_it_area VARCHAR,
                    vp VARCHAR,
                    team_admin VARCHAR,
                    use_case VARCHAR,
                    use_case_status VARCHAR,
                    databricks VARCHAR,
                    month_onboarded_db DATE,
                    snowflake VARCHAR,
                    month_onboarded_sf DATE,
                    north_star_domain VARCHAR,
                    business_or_it VARCHAR,
                    centerwell_or_insurance VARCHAR,
                    git_repo VARCHAR,
                    unique_identifier VARCHAR,
                    associated_ado_items VARCHAR,
                    team_artifacts VARCHAR,
                    current_tech_stack VARCHAR,
                    ad_groups VARCHAR,
                    notes TEXT,
                    csm VARCHAR,
                    health VARCHAR,
                    health_reason VARCHAR
                )
            """))
            conn.commit()
            print("✅ accounts table created")
            
            # Create use_cases table with ALL columns from models.py
            print("\n📋 Creating use_cases table...")
            conn.execute(text("""
                CREATE TABLE use_cases (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    problem TEXT,
                    solution TEXT,
                    value VARCHAR,
                    leader VARCHAR,
                    status VARCHAR,
                    enablement_tier VARCHAR,
                    platform VARCHAR
                )
            """))
            conn.commit()
            print("✅ use_cases table created")
            
            # Create updates table with ALL columns from models.py
            print("\n📋 Creating updates table...")
            conn.execute(text("""
                CREATE TABLE updates (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    description TEXT,
                    author VARCHAR,
                    platform VARCHAR,
                    date DATE
                )
            """))
            conn.commit()
            print("✅ updates table created")
            
            # Create platforms_crm table with ALL columns from models.py
            print("\n📋 Creating platforms_crm table...")
            conn.execute(text("""
                CREATE TABLE platforms_crm (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    platform_name VARCHAR,
                    onboarding_status VARCHAR
                )
            """))
            conn.commit()
            print("✅ platforms_crm table created")
            
            # Create primary_it_partners table with ALL columns from models.py
            print("\n📋 Creating primary_it_partners table...")
            conn.execute(text("""
                CREATE TABLE primary_it_partners (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    primary_it_partner VARCHAR
                )
            """))
            conn.commit()
            print("✅ primary_it_partners table created")
            
            # Create request_states table with ALL columns from models.py
            print("\n📋 Creating request_states table...")
            conn.execute(text("""
                CREATE TABLE request_states (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL UNIQUE,
                    color VARCHAR,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ request_states table created")
            
            # Create intake_requests table with ALL columns from models.py
            print("\n📋 Creating intake_requests table...")
            conn.execute(text("""
                CREATE TABLE intake_requests (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    description TEXT,
                    has_it_partner BOOLEAN DEFAULT FALSE,
                    dri_contact VARCHAR,
                    submitted_for VARCHAR,
                    functional_area VARCHAR,
                    help_types VARCHAR,
                    platform VARCHAR,
                    additional_details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ intake_requests table created")
            
            # Create request_state_assignments table with ALL columns from models.py
            print("\n📋 Creating request_state_assignments table...")
            conn.execute(text("""
                CREATE TABLE request_state_assignments (
                    id SERIAL PRIMARY KEY,
                    request_id INTEGER NOT NULL REFERENCES intake_requests(id) ON DELETE CASCADE,
                    state_id INTEGER NOT NULL REFERENCES request_states(id) ON DELETE CASCADE,
                    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ request_state_assignments table created")
            
            # Insert default request states
            print("\n📝 Inserting default request states...")
            conn.execute(text("""
                INSERT INTO request_states (name, description, color) VALUES
                    ('New', 'Request has been submitted and is awaiting review', '#3b82f6'),
                    ('In Review', 'Request is being reviewed by the team', '#8b5cf6'),
                    ('Assigned', 'Request has been assigned to a team member', '#0ea5e9'),
                    ('In Progress', 'Work on the request has started', '#f59e0b'),
                    ('Blocked', 'Request is blocked and cannot proceed', '#ef4444'),
                    ('Completed', 'Request has been successfully completed', '#10b981'),
                    ('Rejected', 'Request has been rejected', '#6b7280')
            """))
            conn.commit()
            print("✅ Default request states inserted")
            
            print("\n" + "=" * 60)
            print("🎉 Migration completed successfully!")
            print("=" * 60)
            print("\nAll tables created with correct schema:")
            print("  ✓ accounts")
            print("  ✓ use_cases")
            print("  ✓ updates")
            print("  ✓ platforms_crm")
            print("  ✓ primary_it_partners")
            print("  ✓ request_states (with 7 default states)")
            print("  ✓ intake_requests")
            print("  ✓ request_state_assignments")
            print("\n📊 Next step: Run 'python seed_azure_db.py' to add sample data")
            print("=" * 60)
            
            return True
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
