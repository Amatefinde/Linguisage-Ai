from fastapi import FastAPI
from src.review_sentence import router as review_sentence_router

app = FastAPI()
app.include_router(review_sentence_router)