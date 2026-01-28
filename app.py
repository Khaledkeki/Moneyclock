from fastapi import FastAPI
from pydantic import BaseModel
from database import create_user, get_user, save_calculation, get_history, update_purchased, get_summary
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return "server is running"

class calculation(BaseModel):
    price: float
    hourly_wage: float
    user_id: str
    item_name: str
    
    

@app.post("/calculation")
async def calc(input:calculation):
    price = input.price
    hourly_wage = input.hourly_wage
    user_id = input.user_id
    item_name = input.item_name

    hours_needed = price / hourly_wage
    
    save_calculation(user_id, item_name, price, hours_needed)

    return {"hours_needed": hours_needed}


class signup(BaseModel):
    email: str
    password: str
    hourly_wage: float


@app.post('/signup')
async def user(input:signup):

    email = input.email
    password = input.password
    hourly_wage = input.hourly_wage


    create_user(email, password, hourly_wage )

    return {"message": "User created succefully"}

class Login(BaseModel):
    email:str
    password:str

@app.post('/login')
async def login(input:Login):
    email = input.email
    password = input.password

    user = get_user(email)

    if user is None:
        return {"Error": "User not found"}
    
    if user[2] == password:
        return{"message": "Login succesful", "hourly_wage": user[3]}
    else:
        return{"Error": "Wrong password"}
    
@app.get("/history/{user_id}")
async def history(user_id: str):
    user = get_history(user_id)

    return user


class Purchase(BaseModel):
    id: int
    purchased: bool


@app.post("/purchase")
async def mark_purchased(input:Purchase):

    update_purchased(input.id, input.purchased)
    return {"message": "purchase status updated"}



@app.get("/summary/{user_id}")
async def summary(user_id: str):
    result = get_summary(user_id)
    return result









    
    



