"""
Fix Platforms Table Schema
This script checks and fixes the platforms table structure if needed.

Usage:
    python fix_platforms_table.py
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def fix_platforms_table():
    """Check and fix platforms table structure"""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found")
        return False
    
    print("🔌 Connecting to database...")
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("✅ Connected successfully")
            
            # Check current columns in platforms table
            print("\n🔍 Checking platforms table structure...")
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'platforms'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            if not columns:
                print("⚠️  Platforms table doesn't exist. Run migrate_db.py first.")
                return False
            
            print("\n📋 Current columns in platforms table:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
            
            # Check if account_uid exists
            column_names = [col[0] for col in columns]
            
            if 'account_uid' in column_names:
                print("\n✅ Platforms table already has correct structure!")
                return True
            
            # Need to fix the table
            print("\n⚠️  Platforms table has incorrect structure")
            print("\n🔧 Fixing platforms table...")
            
            # Drop and recreate with correct structure
            conn.execute(text("DROP TABLE IF EXISTS platforms CASCADE"))
            conn.commit()
            print("  - Dropped old platforms table")
            
            conn.execute(text("""
                CREATE TABLE platforms (
                    id SERIAL PRIMARY KEY,
                    account_uid VARCHAR NOT NULL REFERENCES accounts(uid) ON DELETE CASCADE,
                    platform_name VARCHAR,
                    onboarding_status VARCHAR
                )
            """))
            conn.commit()
            print("  - Created new platforms table with correct structure")
            
            print("\n✅ Platforms table fixed!")
            print("\nNext step: Run seed_azure_db.py to populate with data")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("Fix Platforms Table Schema")
    print("=" * 60)
    
    success = fix_platforms_table()
    
    if not success:
        exit(1)
