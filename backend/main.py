from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import BaseModel
from datetime import date as date_type
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from database import create_db_and_tables, get_session, engine
from models import Account, UseCase, Update, Platform, PrimaryITPartner, IntakeRequest, RequestState, RequestStateAssignment


class AccountUpdate(BaseModel):
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


class UseCaseUpdate(BaseModel):
    account_uid: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    value: Optional[str] = None
    leader: Optional[str] = None
    status: Optional[str] = None
    enablement_tier: Optional[str] = None
    platform: Optional[str] = None


class UpdateUpdate(BaseModel):
    account_uid: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    platform: Optional[str] = None
    date: Optional[date_type] = None


class PlatformUpdate(BaseModel):
    account_uid: Optional[str] = None
    platform_name: Optional[str] = None
    onboarding_status: Optional[str] = None


class PrimaryITPartnerUpdate(BaseModel):
    account_uid: Optional[str] = None
    primary_it_partner: Optional[str] = None


class IntakeRequestCreate(BaseModel):
    title: str
    description: Optional[str] = None
    has_it_partner: bool = False
    dri_contact: Optional[str] = None
    submitted_for: Optional[str] = None
    functional_area: Optional[str] = None
    help_types: Optional[str] = None
    platform: Optional[str] = None


class IntakeRequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    has_it_partner: Optional[bool] = None
    dri_contact: Optional[str] = None
    submitted_for: Optional[str] = None
    functional_area: Optional[str] = None
    help_types: Optional[str] = None
    platform: Optional[str] = None


class RequestStateCreate(BaseModel):
    name: str
    color: Optional[str] = None
    description: Optional[str] = None


class RequestStateUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


from sample_data import (
    get_sample_accounts,
    get_sample_use_cases,
    get_sample_updates,
    get_sample_platforms,
    get_sample_primary_it_partners
)

app = FastAPI(title="CRM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USE_SAMPLE_DATA = os.getenv("USE_SAMPLE_DATA", "false").lower() == "true"


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    if not USE_SAMPLE_DATA:
        with Session(engine) as session:
            existing_accounts = session.exec(select(Account)).first()
            if not existing_accounts:
                for account in get_sample_accounts():
                    session.add(account)
                for use_case in get_sample_use_cases():
                    session.add(use_case)
                for update in get_sample_updates():
                    session.add(update)
                for platform in get_sample_platforms():
                    session.add(platform)
                for partner in get_sample_primary_it_partners():
                    session.add(partner)
                session.commit()
            
            existing_states = session.exec(select(RequestState)).first()
            if not existing_states:
                from datetime import datetime
                default_states = [
                    RequestState(name="New", color="#3b82f6", description="Newly submitted request", created_at=datetime.utcnow()),
                    RequestState(name="In Review", color="#f59e0b", description="Under review by admin", created_at=datetime.utcnow()),
                    RequestState(name="Assigned", color="#8b5cf6", description="Assigned to a team member", created_at=datetime.utcnow()),
                    RequestState(name="In Progress", color="#06b6d4", description="Work has started", created_at=datetime.utcnow()),
                    RequestState(name="Blocked", color="#ef4444", description="Waiting on external dependency", created_at=datetime.utcnow()),
                    RequestState(name="Completed", color="#10b981", description="Request has been fulfilled", created_at=datetime.utcnow()),
                    RequestState(name="Rejected", color="#6b7280", description="Request has been declined", created_at=datetime.utcnow()),
                ]
                for state in default_states:
                    session.add(state)
                session.commit()


@app.get("/")
def read_root():
    return {"message": "CRM API is running", "use_sample_data": USE_SAMPLE_DATA}


@app.get("/api/accounts", response_model=List[Account])
def get_accounts(session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        return get_sample_accounts()
    accounts = session.exec(select(Account)).all()
    return accounts


@app.get("/api/accounts/{uid}", response_model=Account)
def get_account(uid: str, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        accounts = get_sample_accounts()
        account = next((a for a in accounts if a.uid == uid), None)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
    
    account = session.get(Account, uid)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.post("/api/accounts", response_model=Account)
def create_account(account: Account, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot create accounts in sample data mode")
    
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@app.put("/api/accounts/{uid}", response_model=Account)
def update_account(uid: str, account: AccountUpdate, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update accounts in sample data mode")
    
    db_account = session.get(Account, uid)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_data = account.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        setattr(db_account, key, value)
    
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@app.delete("/api/accounts/{uid}")
def delete_account(uid: str, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot delete accounts in sample data mode")
    
    account = session.get(Account, uid)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    session.exec(select(UseCase).where(UseCase.account_uid == uid)).all()
    for use_case in session.exec(select(UseCase).where(UseCase.account_uid == uid)):
        session.delete(use_case)
    
    for update in session.exec(select(Update).where(Update.account_uid == uid)):
        session.delete(update)
    
    for platform in session.exec(select(Platform).where(Platform.account_uid == uid)):
        session.delete(platform)
    
    for partner in session.exec(select(PrimaryITPartner).where(PrimaryITPartner.account_uid == uid)):
        session.delete(partner)
    
    session.delete(account)
    session.commit()
    return {"ok": True}


@app.get("/api/accounts/{uid}/use-cases", response_model=List[UseCase])
def get_account_use_cases(uid: str, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        use_cases = get_sample_use_cases()
        return [uc for uc in use_cases if uc.account_uid == uid]
    
    use_cases = session.exec(select(UseCase).where(UseCase.account_uid == uid)).all()
    return use_cases


@app.post("/api/use-cases", response_model=UseCase)
def create_use_case(use_case: UseCase, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot create use cases in sample data mode")
    
    session.add(use_case)
    session.commit()
    session.refresh(use_case)
    return use_case


@app.put("/api/use-cases/{id}", response_model=UseCase)
def update_use_case(id: int, use_case: UseCaseUpdate, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update use cases in sample data mode")
    
    db_use_case = session.get(UseCase, id)
    if not db_use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    
    use_case_data = use_case.model_dump(exclude_unset=True)
    for key, value in use_case_data.items():
        setattr(db_use_case, key, value)
    
    session.add(db_use_case)
    session.commit()
    session.refresh(db_use_case)
    return db_use_case


@app.delete("/api/use-cases/{id}")
def delete_use_case(id: int, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot delete use cases in sample data mode")
    
    use_case = session.get(UseCase, id)
    if not use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    
    session.delete(use_case)
    session.commit()
    return {"ok": True}


@app.get("/api/accounts/{uid}/updates", response_model=List[Update])
def get_account_updates(uid: str, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        updates = get_sample_updates()
        return [u for u in updates if u.account_uid == uid]
    
    updates = session.exec(select(Update).where(Update.account_uid == uid)).all()
    return updates


@app.post("/api/updates", response_model=Update)
def create_update(update: Update, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot create updates in sample data mode")
    
    session.add(update)
    session.commit()
    session.refresh(update)
    return update


@app.put("/api/updates/{id}", response_model=Update)
def update_update(id: int, update: UpdateUpdate, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update updates in sample data mode")
    
    db_update = session.get(Update, id)
    if not db_update:
        raise HTTPException(status_code=404, detail="Update not found")
    
    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_update, key, value)
    
    session.add(db_update)
    session.commit()
    session.refresh(db_update)
    return db_update


@app.delete("/api/updates/{id}")
def delete_update(id: int, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot delete updates in sample data mode")
    
    update = session.get(Update, id)
    if not update:
        raise HTTPException(status_code=404, detail="Update not found")
    
    session.delete(update)
    session.commit()
    return {"ok": True}


@app.get("/api/accounts/{uid}/platforms", response_model=List[Platform])
def get_account_platforms(uid: str, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        platforms = get_sample_platforms()
        return [p for p in platforms if p.account_uid == uid]
    
    platforms = session.exec(select(Platform).where(Platform.account_uid == uid)).all()
    return platforms


@app.post("/api/platforms", response_model=Platform)
def create_platform(platform: Platform, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot create platforms in sample data mode")
    
    session.add(platform)
    session.commit()
    session.refresh(platform)
    return platform


@app.put("/api/platforms/{id}", response_model=Platform)
def update_platform(id: int, platform: PlatformUpdate, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update platforms in sample data mode")
    
    db_platform = session.get(Platform, id)
    if not db_platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    platform_data = platform.model_dump(exclude_unset=True)
    for key, value in platform_data.items():
        setattr(db_platform, key, value)
    
    session.add(db_platform)
    session.commit()
    session.refresh(db_platform)
    return db_platform


@app.delete("/api/platforms/{id}")
def delete_platform(id: int, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot delete platforms in sample data mode")
    
    platform = session.get(Platform, id)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    session.delete(platform)
    session.commit()
    return {"ok": True}


@app.get("/api/accounts/{uid}/primary-it-partner", response_model=PrimaryITPartner)
def get_account_primary_it_partner(uid: str, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        partners = get_sample_primary_it_partners()
        partner = next((p for p in partners if p.account_uid == uid), None)
        if not partner:
            raise HTTPException(status_code=404, detail="Primary IT Partner not found")
        return partner
    
    partner = session.exec(select(PrimaryITPartner).where(PrimaryITPartner.account_uid == uid)).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Primary IT Partner not found")
    return partner


@app.post("/api/primary-it-partners", response_model=PrimaryITPartner)
def create_primary_it_partner(partner: PrimaryITPartner, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot create primary IT partners in sample data mode")
    
    session.add(partner)
    session.commit()
    session.refresh(partner)
    return partner


@app.put("/api/primary-it-partners/{id}", response_model=PrimaryITPartner)
def update_primary_it_partner(id: int, partner: PrimaryITPartnerUpdate, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update primary IT partners in sample data mode")
    
    db_partner = session.get(PrimaryITPartner, id)
    if not db_partner:
        raise HTTPException(status_code=404, detail="Primary IT Partner not found")
    
    partner_data = partner.model_dump(exclude_unset=True)
    for key, value in partner_data.items():
        setattr(db_partner, key, value)
    
    session.add(db_partner)
    session.commit()
    session.refresh(db_partner)
    return db_partner


@app.delete("/api/primary-it-partners/{id}")
def delete_primary_it_partner(id: int, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot delete primary IT partners in sample data mode")
    
    partner = session.get(PrimaryITPartner, id)
    if not partner:
        raise HTTPException(status_code=404, detail="Primary IT Partner not found")
    
    session.delete(partner)
    session.commit()
    return {"ok": True}


@app.get("/api/intake-requests", response_model=List[IntakeRequest])
def get_intake_requests(session: Session = Depends(get_session)):
    requests = session.exec(select(IntakeRequest).order_by(IntakeRequest.created_at.desc())).all()
    return requests


@app.get("/api/intake-requests/{id}", response_model=IntakeRequest)
def get_intake_request(id: int, session: Session = Depends(get_session)):
    request = session.get(IntakeRequest, id)
    if not request:
        raise HTTPException(status_code=404, detail="Intake request not found")
    return request


@app.post("/api/intake-requests", response_model=IntakeRequest)
def create_intake_request(request: IntakeRequestCreate, session: Session = Depends(get_session)):
    from datetime import datetime
    
    db_request = IntakeRequest(**request.model_dump())
    db_request.created_at = datetime.utcnow()
    db_request.updated_at = datetime.utcnow()
    
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    
    admin_email = os.getenv("ADMIN_EMAIL")
    if admin_email:
        pass
    
    return db_request


@app.put("/api/intake-requests/{id}", response_model=IntakeRequest)
def update_intake_request(id: int, request: IntakeRequestUpdate, session: Session = Depends(get_session)):
    from datetime import datetime
    
    db_request = session.get(IntakeRequest, id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Intake request not found")
    
    request_data = request.model_dump(exclude_unset=True)
    for key, value in request_data.items():
        setattr(db_request, key, value)
    
    db_request.updated_at = datetime.utcnow()
    
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request


@app.delete("/api/intake-requests/{id}")
def delete_intake_request(id: int, session: Session = Depends(get_session)):
    db_request = session.get(IntakeRequest, id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Intake request not found")
    
    session.exec(select(RequestStateAssignment).where(RequestStateAssignment.request_id == id)).all()
    for assignment in session.exec(select(RequestStateAssignment).where(RequestStateAssignment.request_id == id)):
        session.delete(assignment)
    
    session.delete(db_request)
    session.commit()
    return {"ok": True}


@app.get("/api/request-states", response_model=List[RequestState])
def get_request_states(session: Session = Depends(get_session)):
    states = session.exec(select(RequestState)).all()
    return states


@app.get("/api/request-states/{id}", response_model=RequestState)
def get_request_state(id: int, session: Session = Depends(get_session)):
    state = session.get(RequestState, id)
    if not state:
        raise HTTPException(status_code=404, detail="Request state not found")
    return state


@app.post("/api/request-states", response_model=RequestState)
def create_request_state(state: RequestStateCreate, session: Session = Depends(get_session)):
    from datetime import datetime
    
    db_state = RequestState(**state.model_dump())
    db_state.created_at = datetime.utcnow()
    
    session.add(db_state)
    session.commit()
    session.refresh(db_state)
    return db_state


@app.put("/api/request-states/{id}", response_model=RequestState)
def update_request_state(id: int, state: RequestStateUpdate, session: Session = Depends(get_session)):
    db_state = session.get(RequestState, id)
    if not db_state:
        raise HTTPException(status_code=404, detail="Request state not found")
    
    state_data = state.model_dump(exclude_unset=True)
    for key, value in state_data.items():
        setattr(db_state, key, value)
    
    session.add(db_state)
    session.commit()
    session.refresh(db_state)
    return db_state


@app.delete("/api/request-states/{id}")
def delete_request_state(id: int, session: Session = Depends(get_session)):
    db_state = session.get(RequestState, id)
    if not db_state:
        raise HTTPException(status_code=404, detail="Request state not found")
    
    for assignment in session.exec(select(RequestStateAssignment).where(RequestStateAssignment.state_id == id)):
        session.delete(assignment)
    
    session.delete(db_state)
    session.commit()
    return {"ok": True}


@app.get("/api/intake-requests/{request_id}/states", response_model=List[RequestState])
def get_request_states_for_intake(request_id: int, session: Session = Depends(get_session)):
    assignments = session.exec(
        select(RequestStateAssignment).where(RequestStateAssignment.request_id == request_id)
    ).all()
    
    state_ids = [assignment.state_id for assignment in assignments]
    states = []
    for state_id in state_ids:
        state = session.get(RequestState, state_id)
        if state:
            states.append(state)
    
    return states


@app.post("/api/intake-requests/{request_id}/states/{state_id}")
def assign_state_to_request(request_id: int, state_id: int, session: Session = Depends(get_session)):
    from datetime import datetime
    
    db_request = session.get(IntakeRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Intake request not found")
    
    db_state = session.get(RequestState, state_id)
    if not db_state:
        raise HTTPException(status_code=404, detail="Request state not found")
    
    existing = session.exec(
        select(RequestStateAssignment).where(
            RequestStateAssignment.request_id == request_id,
            RequestStateAssignment.state_id == state_id
        )
    ).first()
    
    if existing:
        return {"ok": True, "message": "State already assigned"}
    
    assignment = RequestStateAssignment(
        request_id=request_id,
        state_id=state_id,
        assigned_at=datetime.utcnow()
    )
    
    session.add(assignment)
    session.commit()
    return {"ok": True}


@app.delete("/api/intake-requests/{request_id}/states/{state_id}")
def remove_state_from_request(request_id: int, state_id: int, session: Session = Depends(get_session)):
    assignment = session.exec(
        select(RequestStateAssignment).where(
            RequestStateAssignment.request_id == request_id,
            RequestStateAssignment.state_id == state_id
        )
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="State assignment not found")
    
    session.delete(assignment)
    session.commit()
    return {"ok": True}


@app.get("/api/functional-areas")
def get_functional_areas():
    return [
        "Finance",
        "Marketing",
        "Sales",
        "Operations",
        "Human Resources",
        "IT",
        "Product",
        "Engineering",
        "Customer Success",
        "Legal",
        "Research & Development",
        "Supply Chain"
    ]
