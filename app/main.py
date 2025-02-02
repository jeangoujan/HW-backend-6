from fastapi import FastAPI, Form, Request, HTTPException, Response, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from .repository import UserRepository, User
from jose import jwt
import json
from .repository import Flower, FlowersRepository



app = FastAPI()
templates = Jinja2Templates(directory="templates")
repo = UserRepository()
fl_repo = FlowersRepository()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 

# Signup -----------------------------------------------------
@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    user = User(email=email, username=username, password=password)
    repo.save_user(user)
    return RedirectResponse(url="/login", status_code=303)
# -------------------------------------------------------------
#Login
@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    user = repo.get_by_username(username)
    if user is None or user.password != password:
        raise HTTPException(status_code=403, detail="Permission denied")
    if user.password == password:
        redirect_response = RedirectResponse(url="/profile", status_code=303)
        token = create_jwt(user.id)
        redirect_response.set_cookie("token", token)
        return redirect_response
# -------------------------------------------------------------


@app.get("/profile")
def profile(request: Request, token: str = Cookie(default=None)):
    if token is None:
        return RedirectResponse(url="/login", status_code=303)
    user_id = decode_jwt(token)
    user = repo.get_by_id(user_id)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})



# JWT --------------------------------------------------------
def create_jwt(user_id: int) -> int:
    body = {"user_id": user_id}
    token = jwt.encode(body, "jeangoujan", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "jeangoujan", "HS256")
    return data["user_id"]
# -------------------------------------------------------------


# Flowers -----------------------------------------------------
@app.get("/flowers")
def flowers(request: Request):
    return templates.TemplateResponse("flowers.html", {"request": request, "flowers": fl_repo.flowers})

@app.post("/flowers")
def flowers(
    request: Request,
    flower_name: str = Form(...),
    quantity: int = Form(...),
    price: int = Form(...)
):
    flower = Flower(flower_name=flower_name, quantity=quantity, price=price)
    fl_repo.save_flower(flower)
    return RedirectResponse(url="/flowers", status_code=303)
# -------------------------------------------------------------

@app.post("/cart/items")
def add_cart(request: Request, flower_id: int = Form()):
        cart_cookie = request.cookies.get("cart_items")

        if cart_cookie:
            cart_items = json.loads(cart_cookie)
        else:
            cart_items = []
        
        if flower_id not in cart_items:
            cart_items.append(flower_id)

        redirect_response = RedirectResponse(url="/flowers", status_code=303)
        redirect_response.set_cookie(key="cart_items", value=json.dumps(cart_items))
        
        return redirect_response



@app.get("/cart/items")
def get_cart(request: Request, cart_items: str = Cookie(default="[]")):
    flower_ids = json.loads(cart_items)
    flowers = []
    for flower_id in flower_ids:
        flower = fl_repo.get_by_id(flower_id)
        if flower:
            flowers.append(flower)
        
    total_price = sum([flower.price for flower in flowers])
    
    return templates.TemplateResponse("cart.html", {"request": request, "flowers": flowers, "total_price": total_price})