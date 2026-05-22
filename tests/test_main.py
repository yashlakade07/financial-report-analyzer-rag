import pytest
from fastapi.testclient import TestClient
from unittest import mock
import io
from app.main import app

client = TestClient(app)

def test_upload_invalid_file_type():
    file_content = b"This is a text file, not a pdf."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/api/v1/upload", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported."

@mock.patch("app.main.process_pdf")
def test_upload_valid_pdf(mock_process_pdf):
    mock_process_pdf.return_value = 5
    file_content = b"%PDF-1.4 dummy pdf content"
    files = {"file": ("report.pdf", io.BytesIO(file_content), "application/pdf")}
    response = client.post("/api/v1/upload", files=files)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully processed report.pdf into 5 data chunks."

@mock.patch("app.main.ask_question")
def test_chat_success(mock_ask_question):
    mock_ask_question.return_value = {
        "answer": "The total revenue was $5 million.",
        "sources": ["Page 1", "Page 3"]
    }
    payload = {"question": "What was the total revenue?"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "The total revenue was $5 million."
    assert "Page 1" in data["sources"]

@mock.patch("app.main.ask_question")
def test_chat_without_processed_document(mock_ask_question):
    mock_ask_question.side_effect = ValueError("No document has been processed yet. Please upload a PDF.")
    payload = {"question": "What was the total revenue?"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "No document has been processed yet. Please upload a PDF."