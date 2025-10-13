from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import os

from database import create_db_and_tables, get_session, engine
from models import Account, UseCase, Update, Platform, PrimaryITPartner
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
def update_account(uid: str, account: Account, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update accounts in sample data mode")
    
    db_account = session.get(Account, uid)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_data = account.dict(exclude_unset=True)
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
def update_use_case(id: int, use_case: UseCase, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update use cases in sample data mode")
    
    db_use_case = session.get(UseCase, id)
    if not db_use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    
    use_case_data = use_case.dict(exclude_unset=True)
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
def update_update(id: int, update: Update, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update updates in sample data mode")
    
    db_update = session.get(Update, id)
    if not db_update:
        raise HTTPException(status_code=404, detail="Update not found")
    
    update_data = update.dict(exclude_unset=True)
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
def update_platform(id: int, platform: Platform, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update platforms in sample data mode")
    
    db_platform = session.get(Platform, id)
    if not db_platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    platform_data = platform.dict(exclude_unset=True)
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
def update_primary_it_partner(id: int, partner: PrimaryITPartner, session: Session = Depends(get_session)):
    if USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="Cannot update primary IT partners in sample data mode")
    
    db_partner = session.get(PrimaryITPartner, id)
    if not db_partner:
        raise HTTPException(status_code=404, detail="Primary IT Partner not found")
    
    partner_data = partner.dict(exclude_unset=True)
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
