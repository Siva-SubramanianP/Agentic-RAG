from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from vectorDbStore import vectorDbStoreFunc
from retrieveLLM import retrievefromLLM
from ChatBot import chatbot
from pydantic import BaseModel #automatic data validation, Parsing and Type coercion
import time

class ChatQuestions(BaseModel):
    question : str

app = FastAPI()

USERNAME = "admin"
PASSWORD = "1234"

app.mount("/static",StaticFiles(directory="static"),name="Static")
templates = Jinja2Templates(directory="templates")

# @app.get("/",response_class=HTMLResponse)
# async def home(request : Request):
#     return templates.TemplateResponse(request,"login.html")


# @app.post("/dashboard",response_class=HTMLResponse)
# async def dashboard(request : Request):
#     form = await request.form()
#     if USERNAME == form["username"] and PASSWORD == form["password"]:
#         return templates.TemplateResponse(request,"dashboard.html")
#     else:
#         return f"""
#         <script>
#             alert("Invalid Username or Password..");
#             window.location.href = "/";
#         </script>
#         """

# @app.get("/dashboard",response_class=HTMLResponse)
# async def get_dashboard(request : Request):
#     return templates.TemplateResponse(request,"dashboard.html")

# @app.post("/upload")
# async def upload_doc(documents: List[UploadFile] = File(...)):

#     message, uploaded_files, failureCount = await vectorDbStoreFunc(documents)
#     return {
#         "message": message,
#         "uploaded": len(uploaded_files),
#         "failed": failureCount,
#         "files": uploaded_files
#     }

# @app.post("/query")
# async def query_ans(request : ChatQuestions):
#     question = request.question
#     answer = await retrievefromLLM(question)
#     return{
#         "answer" : answer
#     }

# @app.api_route("/chat",methods=["GET","POST"] ,response_class=HTMLResponse)
# async def chatBot(request : Request):
#     return templates.TemplateResponse(request,"chat.html")

# @app.post("/botchat")
# async def botchat(request : ChatQuestions):
#     question = request.question
#     answer = await chatbot(question)
#     return{
#         "answer" : answer
#     }

@app.get("/",response_class=HTMLResponse)
async def health():
    return f"""<center><h2>Hello, World</h2></center>"""

# @app.post("/botchat")
# async def botchat(data:dict):

#     question = data["question"]

#     answer = await chatbot(question)

#     def generate():
#         for word in answer.split():
#             yield word + " "
#             time.sleep(0.1)

#     return StreamingResponse(
#         generate(),
#         media_type="text/plain"
#     )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app",reload=True)
