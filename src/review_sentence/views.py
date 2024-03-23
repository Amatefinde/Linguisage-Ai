from fastapi import APIRouter
from .llm_provider import do_review

router = APIRouter(tags=['Review Sentence'], prefix='/review-sentence')


@router.get("")
async def review(word: str, sense: str, sentence: str):
    return do_review(word, sense, sentence)



