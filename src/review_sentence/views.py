from fastapi import APIRouter
from .llm_provider import do_review
from .types import ReviewRequest
router = APIRouter(tags=['Review Sentence'], prefix='/review-sentence')


@router.post("")
async def review(review_request: ReviewRequest):
    return do_review(review_request.word, review_request.sense, review_request.sentence)



