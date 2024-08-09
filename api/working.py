from fastapi import FastAPI, Query, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, String, Integer, Date, Float, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased
from pydantic import BaseModel
from datetime import date, timedelta, datetime
import json
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "73314982e2116c8861b6ab4c21b4e23b628b1b7bc07199c589d6b6414b6729d2")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

db = {
    "osman": {
        "username": "osman",
        "full_name": "Osman Gurel",
        "email": "osmangurel@example.com",
        "hashed_password": "$2b$12$nhrMpuZupi.btRHhXjHYoeoIILjLnPWFg1itURlXSm1.jU3fLxebu",
        "disabled": False
    },
    "isil": {
        "username": "isil",
        "full_name": "isil erkisi",
        "email": "erkisiisil@example.com",
        "hashed_password": "$2b$12$nhrMpuZupi.btRHhXjHYoeoIILjLnPWFg1itURlXSm1.jU3fLxebu", 
        "disabled": True
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

# updated codes for environmental variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "çalışıyor"}



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://hr-task-user:adinTask2024!@hr-task-db.cqbarc8xc1jj.us-east-1.rds.amazonaws.com/hr-task")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class DailyCampaign(Base):
    __tablename__ = "tbl_daily_campaigns"
    campaign_id = Column(String(50), primary_key=True)
    campaign_name = Column(String(100))
    date = Column(Date)
    views = Column(Integer)
    impressions = Column(Integer)
    cpm = Column(Integer)
    clicks = Column(Integer)

class DailyScores(Base):
    __tablename__ = "tbl_daily_scores"
    campaign_id = Column(String(50), primary_key=True)
    campaign_name = Column(String(100))
    date = Column(Date)
    media = Column(Integer)
    creative = Column(Integer)
    effectiveness = Column(Integer)

class CampaignDataResponse(BaseModel):
    campaign_id: str
    campaign_name: str
    date: date
    views: int
    impressions: int
    cpm: int
    clicks: int
    media: int
    creative: int
    effectiveness: int

def get_campaign_data(session, campaign_id=None, start_date=None, end_date=None):
    DC = aliased(DailyCampaign)
    DS = aliased(DailyScores)

    query = session.query(
        DC.campaign_id,
        DC.campaign_name,
        DC.date,
        DC.views,
        DC.impressions,
        DC.cpm,
        DC.clicks,
        DS.media,
        DS.creative,
        DS.effectiveness
    ).join(DS, and_(DS.campaign_id == DC.campaign_id, DC.date == DS.date))

    if campaign_id:
        query = query.filter(DC.campaign_id == DS.campaign_id)
    
    if start_date:
        query = query.filter(DC.date >= start_date)
    
    if end_date:
        query = query.filter(DC.date <= end_date)

    results = query.all()

    response = []
    for result in results:
        response.append(
            {
                "campaign_id": result.campaign_id,
                "campaign_name": result.campaign_name,
                "date": str(result.date),
                "views": result.views,
                "impressions": result.impressions,
                "cpm": result.cpm,
                "clicks": result.clicks,
                "media": result.media,
                "creative": result.creative,
                "effectiveness": result.effectiveness
            }
        )
    
    return response

@app.get("/campaign-data")
def api_campaign_data(
    campaign_id: Optional[str] = Query(None), 
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_active_user)
):  

    session = Session()
    data = get_campaign_data(session, campaign_id, start_date, end_date)
    save_response_to_file(data)
    return data


def save_response_to_file(data):
    with open('response.json', 'w') as f:
        json.dump(data, f, indent=3)
