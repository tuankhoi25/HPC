from fastapi import FastAPI
from pydantic import BaseModel
from api.predict import get_dataframes, get_user_info

rfm, df_users = get_dataframes()

app = FastAPI()

# Route GET cơ bản
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Định nghĩa schema đầu vào bằng Pydantic
class UserRequest(BaseModel):
    user_id: int

# POST endpoint nhận user_id
@app.post("/get-user/")
def get_user(request: UserRequest):
    user_info = get_user_info(user_id=request.user_id, rfm=rfm, df_users=df_users)
    return user_info
