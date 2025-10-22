#!/usr/bin/env python3
"""
Azure Database Seeding Script

Seeds Azure PostgreSQL database with sample data for the CRM application.
All columns match exactly with migrate_db.py schema.

Usage:
    python seed_azure_db.py

Make sure your Azure DATABASE_URL is set in .env file or environment variables.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def seed_database():
    """Seed Azure PostgreSQL database with sample data"""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL in your .env file")
        return False
    
    print("=" * 60)
    print("Azure Database Seeding Script")
    print("=" * 60)
    print(f"\n🔌 Connecting to database...")
    print(f"📍 {database_url.split('@')[1] if '@' in database_url else 'database'}")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Connected successfully\n")
            
            # Insert accounts with ALL columns matching migration script
            print("📝 Inserting sample accounts...")
            conn.execute(text("""
                INSERT INTO accounts (
                    uid, team, business_it_area, vp, team_admin,
                    use_case, use_case_status, databricks, month_onboarded_db,
                    snowflake, month_onboarded_sf, north_star_domain, business_or_it,
                    centerwell_or_insurance, git_repo, unique_identifier, associated_ado_items,
                    team_artifacts, current_tech_stack, ad_groups, notes, csm, health, health_reason
                )
                VALUES 
                    ('ACC001', 'Data Analytics Team', 'Business Intelligence', 'Sarah Johnson', 'Mike Chen',
                     'Customer Behavior Analysis', 'Active', 'y', '2024-03-15',
                     'y', '2024-02-10', 'Customer Insights', 'Business',
                     'Insurance', 'https://github.com/company/analytics-dashboard', 'DA-2024-001', 
                     'https://dev.azure.com/items/12345', 'https://confluence.company.com/analytics',
                     'Python, Databricks, Snowflake, Power BI', 'DA-Analytics-Users, DA-Analytics-Admins',
                     'Team is progressing well with Databricks migration', 'Mike Chen', 'Green', 
                     'All systems operational'),
                    
                    ('ACC002', 'Marketing Automation', 'Marketing Technology', 'Robert Davis', 'Lisa Anderson',
                     'Campaign Performance Tracking', 'In Progress', 'y', '2024-01-20',
                     'n', NULL, 'Marketing ROI', 'Business',
                     'Centerwell', 'https://github.com/company/marketing-analytics', 'MA-2024-002',
                     'https://dev.azure.com/items/12346', 'https://confluence.company.com/marketing',
                     'Snowflake, Power Platform, SQL Server', 'MA-Users, MA-Admins',
                     'Successfully migrated to Power Platform', 'Lisa Anderson', 'Yellow',
                     'Awaiting Snowflake onboarding'),
                    
                    ('ACC003', 'Finance Reporting', 'Financial Analytics', 'Emily Taylor', 'James Wilson',
                     'Financial Forecasting Model', 'Planning', 'y', '2024-04-01',
                     'y', '2024-03-25', 'Financial Planning', 'IT',
                     'Insurance', 'https://github.com/company/finance-forecasting', 'FR-2024-003',
                     'https://dev.azure.com/items/12347', 'https://confluence.company.com/finance',
                     'Databricks, Snowflake, Fabric, Excel', 'FR-Users, FR-Power-Users',
                     'Evaluating Fabric integration options', 'James Wilson', 'Green',
                     'On track with all deliverables')
            """))
            conn.commit()
            print("✅ Sample accounts inserted (3 accounts)\n")
            
            # Insert use cases
            print("📝 Inserting sample use cases...")
            conn.execute(text("""
                INSERT INTO use_cases (account_uid, problem, solution, value, leader, status, enablement_tier, platform)
                VALUES 
                    ('ACC001', 'Lack of real-time customer insights', 
                     'Build unified analytics platform with Databricks',
                     '$2M annual savings, 50% faster insights', 'Mike Chen', 'In Progress', 'Tier 2', 'Databricks'),
                    ('ACC002', 'Manual campaign reporting process',
                     'Automated reporting with Power Platform',
                     '80% reduction in reporting time', 'Lisa Anderson', 'Completed', 'Tier 1', 'Power Platform'),
                    ('ACC003', 'Inaccurate financial forecasts',
                     'ML-powered forecasting on Databricks',
                     '30% improvement in forecast accuracy', 'James Wilson', 'Planning', 'Tier 3', 'Databricks')
            """))
            conn.commit()
            print("✅ Sample use cases inserted (3 use cases)\n")
            
            # Insert updates
            print("📝 Inserting sample updates...")
            conn.execute(text("""
                INSERT INTO updates (account_uid, description, author, platform, date)
                VALUES 
                    ('ACC001', 'Completed Phase 1 of Databricks migration', 'Mike Chen', 'Databricks', '2024-03-20'),
                    ('ACC002', 'Campaign dashboard deployed to production', 'Lisa Anderson', 'Power Platform', '2024-02-15'),
                    ('ACC003', 'Databricks workspace setup completed', 'James Wilson', 'Databricks', '2024-04-05')
            """))
            conn.commit()
            print("✅ Sample updates inserted (3 updates)\n")
            
            # Insert platforms
            print("📝 Inserting sample platforms...")
            conn.execute(text("""
                INSERT INTO platforms_crm (account_uid, platform_name, onboarding_status)
                VALUES 
                    ('ACC001', 'Databricks', 'Onboarded'),
                    ('ACC001', 'Snowflake', 'Onboarded'),
                    ('ACC002', 'Databricks', 'Onboarded'),
                    ('ACC002', 'Power Platform', 'In Progress'),
                    ('ACC003', 'Databricks', 'Onboarded'),
                    ('ACC003', 'Snowflake', 'Onboarded')
            """))
            conn.commit()
            print("✅ Sample platforms inserted (6 platform records)\n")
            
            # Insert IT partners
            print("📝 Inserting sample IT partners...")
            conn.execute(text("""
                INSERT INTO primary_it_partners (account_uid, primary_it_partner)
                VALUES 
                    ('ACC001', 'John Smith'),
                    ('ACC002', 'Alice Cooper'),
                    ('ACC003', 'Bob Martinez')
            """))
            conn.commit()
            print("✅ Sample IT partners inserted (3 IT partners)\n")
            
            # Insert intake requests with ALL columns
            print("📝 Inserting sample intake requests...")
            today = datetime.now()
            conn.execute(text("""
                INSERT INTO intake_requests (
                    title, description, functional_area, dri_contact, 
                    submitted_for, has_it_partner, help_types, platform,
                    created_at, updated_at
                )
                VALUES 
                    ('Need Databricks Access for Sales Analytics', 
                     'Our sales team needs access to Databricks for building sales forecasting models',
                     'Sales', 'Jennifer Lee', 'jennifer.lee@company.com', false, 
                     'Platform Access,Training', 'Databricks',
                     :date1, :date1),
                    ('Power BI Dashboard Consultation',
                     'Looking for help designing executive dashboard in Power BI',
                     'Finance', 'Michael Chang', 'michael.chang@company.com', true,
                     'Consultation/Questions,Environment Enhancement', 'Power Platform',
                     :date2, :date2)
            """), {
                'date1': (today - timedelta(hours=17)),
                'date2': (today - timedelta(hours=18))
            })
            conn.commit()
            print("✅ Sample intake requests inserted (2 requests)\n")
            
            # Assign states to requests
            print("📝 Assigning states to intake requests...")
            conn.execute(text("""
                INSERT INTO request_state_assignments (request_id, state_id)
                SELECT ir.id, rs.id
                FROM intake_requests ir
                CROSS JOIN request_states rs
                WHERE ir.title = 'Need Databricks Access for Sales Analytics' 
                AND rs.name = 'New'
                
                UNION ALL
                
                SELECT ir.id, rs.id
                FROM intake_requests ir
                CROSS JOIN request_states rs
                WHERE ir.title = 'Power BI Dashboard Consultation' 
                AND rs.name = 'In Review'
            """))
            conn.commit()
            print("✅ State assignments created (2 assignments)\n")
            
            # Get final counts
            print("=" * 60)
            print("📊 Final Database Summary")
            print("=" * 60)
            result = conn.execute(text("SELECT COUNT(*) FROM accounts"))
            print(f"  ✓ Accounts: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM use_cases"))
            print(f"  ✓ Use Cases: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM updates"))
            print(f"  ✓ Updates: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM platforms_crm"))
            print(f"  ✓ Platform records: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM primary_it_partners"))
            print(f"  ✓ IT Partners: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM request_states"))
            print(f"  ✓ Request States: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM intake_requests"))
            print(f"  ✓ Intake Requests: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM request_state_assignments"))
            print(f"  ✓ State Assignments: {result.scalar()}")
            
            print("\n" + "=" * 60)
            print("🎉 Database seeding completed successfully!")
            print("=" * 60)
            print("\n✅ All done! Your database is ready with sample data.")
            print("\nNext steps:")
            print("  1. Start the backend: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
            print("  2. Start the frontend: npm run dev")
            print("  3. Access the app: http://localhost:5000")
            print("=" * 60 + "\n")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Seeding failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = seed_database()
    import sys
    sys.exit(0 if success else 1)
