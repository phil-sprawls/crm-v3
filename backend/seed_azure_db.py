"""
Azure Database Seeding Script
Seeds an Azure PostgreSQL database with sample data for the CRM application.
Handles partially seeded databases intelligently.

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
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL in your .env file")
        return False
    
    print(f"🔌 Connecting to Azure PostgreSQL database...")
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("✅ Connected successfully")
            
            # Check and insert accounts
            print("\n🔍 Checking accounts table...")
            result = conn.execute(text("SELECT COUNT(*) FROM accounts"))
            account_count = result.scalar()
            
            if account_count and account_count > 0:
                print(f"ℹ️  Found {account_count} existing accounts, adding sample accounts if not present...")
            else:
                print("📝 Accounts table is empty, inserting sample accounts...")
            
            conn.execute(text("""
                INSERT INTO accounts (uid, team, business_it_area, vp, team_admin, 
                                     use_case, use_case_status, databricks, snowflake,
                                     csm, health, health_reason)
                VALUES 
                    ('ACC001', 'Data Analytics Team', 'Business Intelligence', 'Sarah Johnson', 
                     'Mike Chen', 'Customer Behavior Analysis', 'Active', 'Onboarded', 'Onboarded',
                     'Mike Chen', 'Green', 'All systems operational'),
                    ('ACC002', 'Marketing Automation', 'Marketing Technology', 'Robert Davis',
                     'Lisa Anderson', 'Campaign Performance Tracking', 'In Progress', 'Onboarded', 'Not Started',
                     'Lisa Anderson', 'Yellow', 'Awaiting Snowflake onboarding'),
                    ('ACC003', 'Finance Reporting', 'Financial Analytics', 'Emily Taylor',
                     'James Wilson', 'Real-time Financial Dashboards', 'Active', 'Onboarded', 'Onboarded',
                     'James Wilson', 'Green', 'All systems operational')
                ON CONFLICT (uid) DO NOTHING
            """))
            conn.commit()
            print("✅ Sample accounts processed")
            
            # Check and insert use cases
            print("\n🔍 Checking use_cases table...")
            result = conn.execute(text("SELECT COUNT(*) FROM use_cases"))
            usecase_count = result.scalar()
            
            if usecase_count and usecase_count > 0:
                print(f"ℹ️  Found {usecase_count} existing use cases, adding sample use cases...")
            else:
                print("📝 Use cases table is empty, inserting sample use cases...")
            
            conn.execute(text("""
                INSERT INTO use_cases (account_uid, problem, solution, value, leader, status, enablement_tier, platform)
                SELECT * FROM (VALUES
                    ('ACC001', 'Manual data analysis taking too long', 'Automated Databricks pipeline', 
                     'Reduced analysis time by 80%', 'Mike Chen', 'Completed', 'Tier 1', 'Databricks'),
                    ('ACC002', 'Difficulty tracking campaign ROI', 'Real-time marketing dashboard',
                     'Improved campaign performance by 25%', 'Lisa Anderson', 'In Progress', 'Tier 2', 'Databricks'),
                    ('ACC003', 'Quarterly reports manually compiled', 'Automated financial reporting',
                     'Reduced reporting time from 5 days to 2 hours', 'James Wilson', 'Completed', 'Tier 1', 'Snowflake')
                ) AS v(account_uid, problem, solution, value, leader, status, enablement_tier, platform)
                WHERE EXISTS (SELECT 1 FROM accounts WHERE uid = v.account_uid)
            """))
            conn.commit()
            print("✅ Sample use cases processed")
            
            # Check and insert updates
            print("\n🔍 Checking updates table...")
            result = conn.execute(text("SELECT COUNT(*) FROM updates"))
            update_count = result.scalar()
            
            if update_count and update_count > 0:
                print(f"ℹ️  Found {update_count} existing updates, adding sample updates...")
            else:
                print("📝 Updates table is empty, inserting sample updates...")
            
            today = datetime.now()
            conn.execute(text("""
                INSERT INTO updates (account_uid, description, author, platform, date)
                SELECT * FROM (VALUES
                    ('ACC001', 'Completed initial data pipeline setup', 'Mike Chen', 'Databricks', :date1),
                    ('ACC002', 'Marketing dashboard in UAT phase', 'Lisa Anderson', 'Databricks', :date2),
                    ('ACC003', 'Financial reports automated and running daily', 'James Wilson', 'Snowflake', :date3)
                ) AS v(account_uid, description, author, platform, date)
                WHERE EXISTS (SELECT 1 FROM accounts WHERE uid = v.account_uid)
            """), {
                'date1': (today - timedelta(days=7)).date(),
                'date2': (today - timedelta(days=3)).date(),
                'date3': (today - timedelta(days=1)).date()
            })
            conn.commit()
            print("✅ Sample updates processed")
            
            # Check and insert platforms
            print("\n🔍 Checking platforms table...")
            result = conn.execute(text("SELECT COUNT(*) FROM platforms"))
            platform_count = result.scalar()
            
            if platform_count and platform_count > 0:
                print(f"ℹ️  Found {platform_count} existing platform records, adding sample platforms...")
            else:
                print("📝 Platforms table is empty, inserting sample platforms...")
            
            conn.execute(text("""
                INSERT INTO platforms (account_uid, platform_name, onboarding_status)
                SELECT * FROM (VALUES
                    ('ACC001', 'Databricks', 'Onboarded'),
                    ('ACC001', 'Snowflake', 'Onboarded'),
                    ('ACC002', 'Databricks', 'Onboarded'),
                    ('ACC002', 'Power Platform', 'In Progress'),
                    ('ACC003', 'Databricks', 'Onboarded'),
                    ('ACC003', 'Snowflake', 'Onboarded')
                ) AS v(account_uid, platform_name, onboarding_status)
                WHERE EXISTS (SELECT 1 FROM accounts WHERE uid = v.account_uid)
                AND NOT EXISTS (
                    SELECT 1 FROM platforms p 
                    WHERE p.account_uid = v.account_uid 
                    AND p.platform_name = v.platform_name
                )
            """))
            conn.commit()
            print("✅ Sample platforms processed")
            
            # Check and insert IT partners
            print("\n🔍 Checking primary_it_partners table...")
            result = conn.execute(text("SELECT COUNT(*) FROM primary_it_partners"))
            partner_count = result.scalar()
            
            if partner_count and partner_count > 0:
                print(f"ℹ️  Found {partner_count} existing IT partners, adding sample IT partners...")
            else:
                print("📝 IT partners table is empty, inserting sample IT partners...")
            
            conn.execute(text("""
                INSERT INTO primary_it_partners (account_uid, primary_it_partner)
                SELECT * FROM (VALUES
                    ('ACC001', 'John Smith'),
                    ('ACC002', 'Sarah Williams'),
                    ('ACC003', 'David Brown')
                ) AS v(account_uid, primary_it_partner)
                WHERE EXISTS (SELECT 1 FROM accounts WHERE uid = v.account_uid)
                AND NOT EXISTS (
                    SELECT 1 FROM primary_it_partners p 
                    WHERE p.account_uid = v.account_uid
                )
            """))
            conn.commit()
            print("✅ Sample IT partners processed")
            
            # Check and insert request states
            print("\n🔍 Checking request_states table...")
            result = conn.execute(text("SELECT COUNT(*) FROM request_states"))
            state_count = result.scalar()
            
            if not state_count or state_count == 0:
                print("📝 Request states table is empty, inserting default states...")
                conn.execute(text("""
                    INSERT INTO request_states (name, description, color) VALUES
                        ('New', 'Request has been submitted and is awaiting review', '#3b82f6'),
                        ('In Review', 'Request is being reviewed by the team', '#8b5cf6'),
                        ('Assigned', 'Request has been assigned to a team member', '#0ea5e9'),
                        ('In Progress', 'Work on the request has started', '#f59e0b'),
                        ('Blocked', 'Request is blocked and cannot proceed', '#ef4444'),
                        ('Completed', 'Request has been successfully completed', '#10b981'),
                        ('Rejected', 'Request has been rejected', '#6b7280')
                    ON CONFLICT (name) DO NOTHING
                """))
                conn.commit()
                print("✅ Default request states inserted")
            else:
                print(f"ℹ️  Found {state_count} existing states, skipping state insertion")
            
            # Check and insert intake requests
            print("\n🔍 Checking intake_requests table...")
            result = conn.execute(text("SELECT COUNT(*) FROM intake_requests"))
            request_count = result.scalar()
            
            if request_count and request_count > 0:
                print(f"ℹ️  Found {request_count} existing intake requests, adding sample requests...")
            else:
                print("📝 Intake requests table is empty, inserting sample requests...")
            
            today = datetime.now()
            conn.execute(text("""
                INSERT INTO intake_requests (title, description, functional_area, dri_contact, 
                                            submitted_for, has_it_partner, help_types, platform,
                                            created_at, updated_at)
                SELECT * FROM (VALUES
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
                ) AS v(title, description, functional_area, dri_contact, submitted_for, 
                       has_it_partner, help_types, platform, created_at, updated_at)
                WHERE NOT EXISTS (
                    SELECT 1 FROM intake_requests ir WHERE ir.title = v.title
                )
            """), {
                'date1': (today - timedelta(hours=17)),
                'date2': (today - timedelta(hours=18))
            })
            conn.commit()
            print("✅ Sample intake requests processed")
            
            # Check and assign states to requests
            print("\n🔍 Checking request_state_assignments table...")
            result = conn.execute(text("SELECT COUNT(*) FROM request_state_assignments"))
            assignment_count = result.scalar()
            
            if assignment_count and assignment_count > 0:
                print(f"ℹ️  Found {assignment_count} existing state assignments, adding sample assignments...")
            else:
                print("📝 State assignments table is empty, assigning states to sample requests...")
            
            conn.execute(text("""
                INSERT INTO request_state_assignments (request_id, state_id)
                SELECT ir.id, rs.id
                FROM intake_requests ir
                CROSS JOIN request_states rs
                WHERE ir.title = 'Need Databricks Access for Sales Analytics' 
                AND rs.name = 'New'
                AND NOT EXISTS (
                    SELECT 1 FROM request_state_assignments rsa 
                    WHERE rsa.request_id = ir.id AND rsa.state_id = rs.id
                )
                
                UNION ALL
                
                SELECT ir.id, rs.id
                FROM intake_requests ir
                CROSS JOIN request_states rs
                WHERE ir.title = 'Power BI Dashboard Consultation' 
                AND rs.name = 'In Review'
                AND NOT EXISTS (
                    SELECT 1 FROM request_state_assignments rsa 
                    WHERE rsa.request_id = ir.id AND rsa.state_id = rs.id
                )
            """))
            conn.commit()
            print("✅ State assignments processed")
            
            # Get final counts
            print("\n📊 Final database summary:")
            result = conn.execute(text("SELECT COUNT(*) FROM accounts"))
            print(f"  - Accounts: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM use_cases"))
            print(f"  - Use Cases: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM updates"))
            print(f"  - Updates: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM platforms"))
            print(f"  - Platform records: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM primary_it_partners"))
            print(f"  - IT Partners: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM request_states"))
            print(f"  - Request States: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM intake_requests"))
            print(f"  - Intake Requests: {result.scalar()}")
            result = conn.execute(text("SELECT COUNT(*) FROM request_state_assignments"))
            print(f"  - State Assignments: {result.scalar()}")
            
            print("\n🎉 Database seeding completed successfully!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: Seeding failed")
        print(f"Error details: {str(e)}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("Azure Database Seeding Script")
    print("=" * 60)
    
    success = seed_database()
    
    if success:
        print("\n✅ All done! Your Azure database is ready with sample data.")
        print("\nNext steps:")
        print("  1. Deploy your backend to Azure App Service")
        print("  2. Test the application with the sample data")
    else:
        print("\n❌ Seeding failed. Please check the error above.")
        exit(1)
