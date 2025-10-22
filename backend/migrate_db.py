#!/usr/bin/env python3
"""
Database migration script for IT Platform CRM

Creates all database tables matching the schema in models.py.
Safe to run multiple times.

Usage:
    python migrate_db.py              # Create tables (safe, preserves data)
    python migrate_db.py --drop       # Drop and recreate all tables (DESTRUCTIVE)
"""

import os
import sys
from sqlalchemy import create_engine, text

def migrate_database(drop_tables=False):
    """Run database migration to create all tables"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("\nPlease set DATABASE_URL in your .env file or environment")
        return False
    
    print("🚀 Starting database migration...")
    print(f"📍 Connecting to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
    
    if drop_tables:
        print("\n⚠️  WARNING: --drop flag detected!")
        print("⚠️  This will DELETE ALL DATA in the following tables:")
        print("    - request_state_assignments")
        print("    - intake_requests")
        print("    - request_states")
        print("    - primary_it_partners")
        print("    - platforms_crm")
        print("    - updates")
        print("    - use_cases")
        print("    - accounts")
        response = input("\n❓ Type 'YES' to confirm deletion: ")
        if response != "YES":
            print("❌ Migration cancelled")
            return False
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            if drop_tables:
                print("\n🗑️  Dropping existing tables...")
                # Drop in reverse dependency order
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
                    print(f"   Dropping {table}...")
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                conn.commit()
                print("✅ All tables dropped")
            
            # Create accounts table (parent table, no dependencies)
            print("\n📋 Creating accounts table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS accounts (
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
            
            # Create use_cases table
            print("\n📋 Creating use_cases table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS use_cases (
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
            
            # Create updates table
            print("\n📋 Creating updates table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS updates (
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
            
            # Create platforms_crm table
            print("\n📋 Creating platforms_crm table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS platforms_crm (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    platform_name VARCHAR,
                    onboarding_status VARCHAR
                )
            """))
            conn.commit()
            print("✅ platforms_crm table created")
            
            # Create primary_it_partners table
            print("\n📋 Creating primary_it_partners table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS primary_it_partners (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    primary_it_partner VARCHAR
                )
            """))
            conn.commit()
            print("✅ primary_it_partners table created")
            
            # Create request_states table
            print("\n📋 Creating request_states table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS request_states (
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
                CREATE TABLE IF NOT EXISTS intake_requests (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    description TEXT,
                    has_it_partner BOOLEAN DEFAULT FALSE,
                    dri_contact VARCHAR,
                    submitted_for VARCHAR,
                    functional_area VARCHAR,
                    help_types VARCHAR,
                    platform VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ request_state_assignments table created")
            
            # Check if default states already exist
            print("\n🔍 Checking for existing request states...")
            result = conn.execute(text("SELECT COUNT(*) FROM request_states"))
            count = result.scalar()
            
            if count and count > 0:
                print(f"ℹ️  Found {count} existing states, skipping default state insertion")
            else:
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
                print("✅ Default states inserted")
            
            print("\n🎉 Migration completed successfully!")
            print("\nAll tables created:")
            print("  - accounts")
            print("  - use_cases")
            print("  - updates")
            print("  - platforms_crm")
            print("  - primary_it_partners")
            print("  - request_states")
            print("  - intake_requests")
            print("  - request_state_assignments")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration - IT Platform CRM")
    print("=" * 60)
    
    drop_tables = "--drop" in sys.argv or "--drop-tables" in sys.argv
    
    success = migrate_database(drop_tables=drop_tables)
    sys.exit(0 if success else 1)
