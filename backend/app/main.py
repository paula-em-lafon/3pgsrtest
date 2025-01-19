from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException 
from app.database import drop_tables, create_tables
from app import views
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend origin
    "http://127.0.0.1:3000", # Alternative localhost format
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins or set ["*"] to allow all
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "now we're cooking"}

@app.post('/initdb')
async def initdb():
    try:
        drop_tables()
        create_tables()
        return {"message": "Tables dropped and created!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error {e}"
        )
    
app.include_router(views.router, prefix='/api', tags=['books'])