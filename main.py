import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client


app = FastAPI()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")



# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/testing/{user_id}")
async def get_user_data(user_id: str):
    try:
        # Query the Supabase table named 'testing' where 'id' matches the user_id
        response = supabase.from_("testing").select("*").eq("id", user_id).execute()
        
        # If no records found, return a 404
        if len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"data": response.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))