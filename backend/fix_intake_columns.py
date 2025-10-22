#!/usr/bin/env python3
"""
Fix intake_requests table columns to match models.py

This script adds missing columns (dri_contact, submitted_for) to the intake_requests table
if they don't exist. Safe to run multiple times.

Usage:
    python fix_intake_columns.py
"""

import os
import sys
from sqlalchemy import create_engine, text

def fix_intake_columns():
    """Add missing columns to intake_requests table"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("\nPlease set DATABASE_URL in your .env file or environment")
        return False
    
    print("🔧 Fixing intake_requests table columns...")
    print(f"📍 Connecting to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if columns exist
            print("\n🔍 Checking existing columns...")
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'intake_requests'
            """))
            existing_columns = {row[0] for row in result}
            print(f"   Found columns: {', '.join(sorted(existing_columns))}")
            
            columns_to_add = []
            
            # Check for dri_contact
            if 'dri_contact' not in existing_columns:
                columns_to_add.append(('dri_contact', 'VARCHAR'))
                print("   ⚠️  Missing: dri_contact")
            
            # Check for submitted_for
            if 'submitted_for' not in existing_columns:
                columns_to_add.append(('submitted_for', 'VARCHAR'))
                print("   ⚠️  Missing: submitted_for")
            
            # Check for help_types
            if 'help_types' not in existing_columns:
                columns_to_add.append(('help_types', 'VARCHAR'))
                print("   ⚠️  Missing: help_types")
            
            if not columns_to_add:
                print("\n✅ All columns already exist - no changes needed!")
                return True
            
            # Add missing columns
            print(f"\n🔨 Adding {len(columns_to_add)} missing column(s)...")
            for column_name, column_type in columns_to_add:
                print(f"   Adding {column_name}...")
                conn.execute(text(f"""
                    ALTER TABLE intake_requests 
                    ADD COLUMN IF NOT EXISTS {column_name} {column_type}
                """))
                conn.commit()
                print(f"   ✅ {column_name} added")
            
            print("\n🎉 Column fix completed successfully!")
            
            # Verify all columns
            print("\n✅ Final verification...")
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'intake_requests'
                ORDER BY ordinal_position
            """))
            all_columns = [row[0] for row in result]
            print(f"   All columns: {', '.join(all_columns)}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Fix Intake Requests Table Columns")
    print("=" * 60)
    
    success = fix_intake_columns()
    sys.exit(0 if success else 1)
