from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date as date_type, datetime


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    
    uid: str = Field(primary_key=True)
    team: Optional[str] = None
    business_it_area: Optional[str] = None
    vp: Optional[str] = None
    team_admin: Optional[str] = None
    use_case: Optional[str] = None
    use_case_status: Optional[str] = None
    databricks: Optional[str] = None
    month_onboarded_db: Optional[date_type] = None
    snowflake: Optional[str] = None
    month_onboarded_sf: Optional[date_type] = None
    north_star_domain: Optional[str] = None
    business_or_it: Optional[str] = None
    centerwell_or_insurance: Optional[str] = None
    git_repo: Optional[str] = None
    unique_identifier: Optional[str] = None
    associated_ado_items: Optional[str] = None
    team_artifacts: Optional[str] = None
    current_tech_stack: Optional[str] = None
    ad_groups: Optional[str] = None
    notes: Optional[str] = None
    csm: Optional[str] = None
    health: Optional[str] = None
    health_reason: Optional[str] = None


class UseCase(SQLModel, table=True):
    __tablename__ = "use_cases"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_uid: str = Field(foreign_key="accounts.uid")
    problem: Optional[str] = None
    solution: Optional[str] = None
    value: Optional[str] = None
    leader: Optional[str] = None
    status: Optional[str] = None
    enablement_tier: Optional[str] = None
    platform: Optional[str] = None


class Update(SQLModel, table=True):
    __tablename__ = "updates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_uid: str = Field(foreign_key="accounts.uid")
    description: Optional[str] = None
    author: Optional[str] = None
    platform: Optional[str] = None
    date: Optional[date_type] = None


class Platform(SQLModel, table=True):
    __tablename__ = "platforms"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_uid: str = Field(foreign_key="accounts.uid")
    platform_name: Optional[str] = None
    onboarding_status: Optional[str] = None


class PrimaryITPartner(SQLModel, table=True):
    __tablename__ = "primary_it_partners"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_uid: str = Field(foreign_key="accounts.uid")
    primary_it_partner: Optional[str] = None
