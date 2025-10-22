"""
Azure Database Seeding Script
Seeds an Azure PostgreSQL database with sample data for the CRM application.

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
            
            # Check if data already exists
            print("\n🔍 Checking for existing data...")
            result = conn.execute(text("SELECT COUNT(*) FROM accounts"))
            account_count = result.scalar()
            
            if account_count and account_count > 0:
                print(f"⚠️  Database already contains {account_count} accounts")
                response = input("Do you want to add more sample data? (y/n): ")
                if response.lower() != 'y':
                    print("❌ Seeding cancelled")
                    return False
            
            # Insert sample accounts
            print("\n📝 Inserting sample accounts...")
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
            print("✅ Sample accounts inserted")
            
            # Insert sample use cases
            print("\n📝 Inserting sample use cases...")
            conn.execute(text("""
                INSERT INTO use_cases (account_uid, problem, solution, value, leader, status, enablement_tier, platform)
                VALUES
                    ('ACC001', 'Manual data analysis taking too long', 'Automated Databricks pipeline', 
                     'Reduced analysis time by 80%', 'Mike Chen', 'Completed', 'Tier 1', 'Databricks'),
                    ('ACC002', 'Difficulty tracking campaign ROI', 'Real-time marketing dashboard',
                     'Improved campaign performance by 25%', 'Lisa Anderson', 'In Progress', 'Tier 2', 'Databricks'),
                    ('ACC003', 'Quarterly reports manually compiled', 'Automated financial reporting',
                     'Reduced reporting time from 5 days to 2 hours', 'James Wilson', 'Completed', 'Tier 1', 'Snowflake')
            """))
            conn.commit()
            print("✅ Sample use cases inserted")
            
            # Insert sample updates
            print("\n📝 Inserting sample updates...")
            today = datetime.now()
            conn.execute(text("""
                INSERT INTO updates (account_uid, description, author, platform, date)
                VALUES
                    ('ACC001', 'Completed initial data pipeline setup', 'Mike Chen', 'Databricks', :date1),
                    ('ACC002', 'Marketing dashboard in UAT phase', 'Lisa Anderson', 'Databricks', :date2),
                    ('ACC003', 'Financial reports automated and running daily', 'James Wilson', 'Snowflake', :date3)
            """), {
                'date1': (today - timedelta(days=7)).date(),
                'date2': (today - timedelta(days=3)).date(),
                'date3': (today - timedelta(days=1)).date()
            })
            conn.commit()
            print("✅ Sample updates inserted")
            
            # Insert sample platforms
            print("\n📝 Inserting sample platform records...")
            conn.execute(text("""
                INSERT INTO platforms (account_uid, platform_name, onboarding_status)
                VALUES
                    ('ACC001', 'Databricks', 'Onboarded'),
                    ('ACC001', 'Snowflake', 'Onboarded'),
                    ('ACC002', 'Databricks', 'Onboarded'),
                    ('ACC002', 'Power Platform', 'In Progress'),
                    ('ACC003', 'Databricks', 'Onboarded'),
                    ('ACC003', 'Snowflake', 'Onboarded')
            """))
            conn.commit()
            print("✅ Sample platforms inserted")
            
            # Insert sample IT partners
            print("\n📝 Inserting sample IT partners...")
            conn.execute(text("""
                INSERT INTO primary_it_partners (account_uid, primary_it_partner)
                VALUES
                    ('ACC001', 'John Smith'),
                    ('ACC002', 'Sarah Williams'),
                    ('ACC003', 'David Brown')
            """))
            conn.commit()
            print("✅ Sample IT partners inserted")
            
            # Insert sample request states (if not already present)
            print("\n📝 Checking request states...")
            result = conn.execute(text("SELECT COUNT(*) FROM request_states"))
            state_count = result.scalar()
            
            if not state_count or state_count == 0:
                print("📝 Inserting default request states...")
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
            else:
                print(f"ℹ️  Found {state_count} existing states, skipping insertion")
            
            # Insert sample intake requests
            print("\n📝 Inserting sample intake requests...")
            today = datetime.now()
            conn.execute(text("""
                INSERT INTO intake_requests (title, description, functional_area, dri_contact, 
                                            submitted_for, has_it_partner, help_types, platform,
                                            created_at, updated_at)
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
            print("✅ Sample intake requests inserted")
            
            # Assign states to requests
            print("\n📝 Assigning states to requests...")
            conn.execute(text("""
                INSERT INTO request_state_assignments (request_id, state_id)
                SELECT ir.id, rs.id
                FROM intake_requests ir
                CROSS JOIN request_states rs
                WHERE ir.title = 'Need Databricks Access for Sales Analytics' AND rs.name = 'New'
                
                UNION ALL
                
                SELECT ir.id, rs.id
                FROM intake_requests ir
                CROSS JOIN request_states rs
                WHERE ir.title = 'Power BI Dashboard Consultation' AND rs.name = 'In Review'
            """))
            conn.commit()
            print("✅ States assigned to requests")
            
            print("\n🎉 Database seeding completed successfully!")
            print("\nSample data created:")
            print("  - 3 Accounts (ACC001, ACC002, ACC003)")
            print("  - 3 Use Cases")
            print("  - 3 Updates")
            print("  - 6 Platform records")
            print("  - 3 IT Partners")
            print("  - 7 Request States")
            print("  - 2 Intake Requests")
            
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
