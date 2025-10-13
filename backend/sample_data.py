from datetime import date
from models import Account, UseCase, Update, Platform, PrimaryITPartner


def get_sample_accounts():
    return [
        Account(
            uid="ACC001",
            team="Data Analytics Team",
            business_it_area="Business Intelligence",
            vp="Sarah Johnson",
            team_admin="Mike Chen",
            use_case="Customer Analytics Dashboard",
            use_case_status="In Progress",
            databricks="y",
            month_onboarded_db=date(2024, 3, 15),
            snowflake="y",
            month_onboarded_sf=date(2024, 2, 10),
            north_star_domain="Customer Insights",
            business_or_it="Business",
            centerwell_or_insurance="Insurance",
            git_repo="https://github.com/company/analytics-dashboard",
            unique_identifier="DA-2024-001",
            associated_ado_items="https://dev.azure.com/items/12345",
            team_artifacts="https://confluence.company.com/analytics",
            current_tech_stack="Python, Databricks, Snowflake, Power BI",
            ad_groups="DA-Analytics-Users, DA-Analytics-Admins",
            notes="Team is progressing well with Databricks migration",
            csm="Jennifer Williams",
            health="Green",
            health_reason="On track with all deliverables"
        ),
        Account(
            uid="ACC002",
            team="Marketing Automation",
            business_it_area="Marketing Technology",
            vp="Robert Davis",
            team_admin="Lisa Anderson",
            use_case="Campaign Performance Analysis",
            use_case_status="Completed",
            databricks="n",
            month_onboarded_db=None,
            snowflake="y",
            month_onboarded_sf=date(2024, 1, 20),
            north_star_domain="Marketing ROI",
            business_or_it="Business",
            centerwell_or_insurance="Centerwell",
            git_repo="https://github.com/company/marketing-analytics",
            unique_identifier="MA-2024-002",
            associated_ado_items="https://dev.azure.com/items/12346",
            team_artifacts="https://confluence.company.com/marketing",
            current_tech_stack="Snowflake, Power Platform, SQL Server",
            ad_groups="MA-Users, MA-Admins",
            notes="Successfully migrated to Snowflake",
            csm="David Brown",
            health="Green",
            health_reason="All systems operational"
        ),
        Account(
            uid="ACC003",
            team="Finance Reporting",
            business_it_area="Financial Analytics",
            vp="Emily Taylor",
            team_admin="James Wilson",
            use_case="Financial Forecasting Model",
            use_case_status="Planning",
            databricks="y",
            month_onboarded_db=date(2024, 4, 1),
            snowflake="n",
            month_onboarded_sf=None,
            north_star_domain="Financial Planning",
            business_or_it="IT",
            centerwell_or_insurance="Insurance",
            git_repo="https://github.com/company/finance-forecasting",
            unique_identifier="FR-2024-003",
            associated_ado_items="https://dev.azure.com/items/12347",
            team_artifacts="https://confluence.company.com/finance",
            current_tech_stack="Databricks, Fabric, Excel",
            ad_groups="FR-Users, FR-Power-Users",
            notes="Evaluating Fabric integration options",
            csm="Amanda Martinez",
            health="Yellow",
            health_reason="Waiting on budget approval for Fabric license"
        )
    ]


def get_sample_use_cases():
    return [
        UseCase(
            account_uid="ACC001",
            problem="Lack of real-time customer insights",
            solution="Build unified analytics platform with Databricks",
            value="$2M annual savings, 50% faster insights",
            leader="Mike Chen",
            status="In Progress",
            enablement_tier="Tier 2",
            platform="Databricks"
        ),
        UseCase(
            account_uid="ACC001",
            problem="Siloed data across multiple systems",
            solution="Centralize data in Snowflake data warehouse",
            value="Single source of truth for customer data",
            leader="Mike Chen",
            status="Completed",
            enablement_tier="Tier 1",
            platform="Snowflake"
        ),
        UseCase(
            account_uid="ACC002",
            problem="Manual campaign reporting process",
            solution="Automated reporting with Snowflake and Power BI",
            value="80% reduction in reporting time",
            leader="Lisa Anderson",
            status="Completed",
            enablement_tier="Tier 1",
            platform="Snowflake"
        ),
        UseCase(
            account_uid="ACC003",
            problem="Inaccurate financial forecasts",
            solution="ML-powered forecasting on Databricks",
            value="30% improvement in forecast accuracy",
            leader="James Wilson",
            status="Planning",
            enablement_tier="Tier 3",
            platform="Databricks"
        )
    ]


def get_sample_updates():
    return [
        Update(
            account_uid="ACC001",
            description="Completed Phase 1 of Databricks migration",
            author="Mike Chen",
            platform="Databricks",
            date=date(2024, 3, 20)
        ),
        Update(
            account_uid="ACC001",
            description="Snowflake data pipeline fully operational",
            author="Sarah Johnson",
            platform="Snowflake",
            date=date(2024, 3, 1)
        ),
        Update(
            account_uid="ACC002",
            description="Campaign dashboard deployed to production",
            author="Lisa Anderson",
            platform="Power Platform",
            date=date(2024, 2, 15)
        ),
        Update(
            account_uid="ACC003",
            description="Databricks workspace setup completed",
            author="James Wilson",
            platform="Databricks",
            date=date(2024, 4, 5)
        )
    ]


def get_sample_platforms():
    return [
        Platform(account_uid="ACC001", platform_name="Databricks", onboarding_status="In Progress"),
        Platform(account_uid="ACC001", platform_name="Snowflake", onboarding_status="Completed"),
        Platform(account_uid="ACC001", platform_name="Power Platform", onboarding_status="Not Started"),
        Platform(account_uid="ACC002", platform_name="Snowflake", onboarding_status="Completed"),
        Platform(account_uid="ACC002", platform_name="Power Platform", onboarding_status="Completed"),
        Platform(account_uid="ACC003", platform_name="Databricks", onboarding_status="In Progress"),
        Platform(account_uid="ACC003", platform_name="Fabric", onboarding_status="Planning")
    ]


def get_sample_primary_it_partners():
    return [
        PrimaryITPartner(account_uid="ACC001", primary_it_partner="John Smith"),
        PrimaryITPartner(account_uid="ACC002", primary_it_partner="Alice Cooper"),
        PrimaryITPartner(account_uid="ACC003", primary_it_partner="Bob Martinez")
    ]
