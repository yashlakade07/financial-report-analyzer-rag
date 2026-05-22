import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.rag import process_pdf, ask_question

app = FastAPI(title="Financial RAG API")

# Ensure a temporary directory exists for uploads
os.makedirs("temp_uploads", exist_ok=True)

@app.post("/api/v1/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = f"temp_uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        chunks_created = process_pdf(file_path)
        return {"message": f"Successfully processed {file.filename} into {chunks_created} data chunks."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = ask_question(request.question)
        return ChatResponse(answer=result["answer"], sources=result["sources"])
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))