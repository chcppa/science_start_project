from datetime import datetime
from typing import List

from fastapi import Depends, APIRouter

from orm.models import FirstModeQuery, FirstModeQueryInDatabase, SecondModeQuery, SecondModeQueryInDatabase, \
    ThirdModeQuery, ThirdModeQueryInDatabase
from services.text_analysis.models import TextRequest, TranslateTextRequest
from services.text_analysis.text_analysis_service import TextAnalysisService
from services.text_analysis.translator_service import TranslatorService
from .service import QueryHistoryService
from ..auth.service import get_current_user_id

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/mode/first/", response_model=FirstModeQuery)
async def first_mode(*, user_id: int = Depends(get_current_user_id),
                     text: TextRequest,
                     query_service: QueryHistoryService = Depends()):
    """
    Route for analyse input text by first mode.
    """
    translator_service = TranslatorService(TranslateTextRequest(text_to_translate=text.text))
    translated_text = await translator_service.text_to_english()

    text_analysis_service = TextAnalysisService(text=translated_text)

    analysis_result = await text_analysis_service.analyse_by_first_mode()

    query_data = dict(
        user_id=user_id,
        **analysis_result.classification_result.dict(),
        original_text=text.text,
        query_date=datetime.utcnow())

    return query_service.create_first_mode_query(query_data)


@router.post("/mode/second/", response_model=SecondModeQuery)
async def second_mode(*, user_id: int = Depends(get_current_user_id),
                      text: TextRequest,
                      query_service: QueryHistoryService = Depends()):
    """
    Route for analyse input text by second mode.
    """
    translator_service = TranslatorService(TranslateTextRequest(text_to_translate=text.text))
    translated_text = await translator_service.text_to_english()

    text_analysis_service = TextAnalysisService(text=translated_text)

    analysis_result = await text_analysis_service.analyse_by_second_mode()

    query_data = dict(
        user_id=user_id,
        **analysis_result.sentiment_analysis_result.dict(),
        **analysis_result.emotion_analysis_result.dict(),
        original_text=text.text,
        query_date=datetime.utcnow())

    return query_service.create_second_mode_query(query_data)


@router.post("/mode/third/", response_model=ThirdModeQuery)
async def third_mode(*, user_id: int = Depends(get_current_user_id),
                     text: TextRequest,
                     query_service: QueryHistoryService = Depends()):
    """
    Route for analyse input text by third mode.
    """
    translator_service = TranslatorService(TranslateTextRequest(text_to_translate=text.text))
    translated_text = await translator_service.text_to_english()

    text_analysis_service = TextAnalysisService(text=translated_text)

    analysis_result = await text_analysis_service.analyse_by_third_mode()

    query_data = dict(
        user_id=user_id,
        **analysis_result.abuse_analysis_result.dict(),
        **analysis_result.emotion_analysis_result.dict(),
        original_text=text.text,
        query_date=datetime.utcnow()
    )

    return query_service.create_third_mode_query(query_data)


@router.get("/mode/first/one", response_model=FirstModeQuery)
async def get_one_of_first_mode(*, user_id: int = Depends(get_current_user_id),
                                query_service: QueryHistoryService = Depends()):
    """
    Route to get the last record of first mode queries history.
    """
    return query_service.get_the_first_mode_query(user_id)


@router.get("/mode/second/one", response_model=ThirdModeQuery)
async def get_one_of_second_mode(*, user_id: int = Depends(get_current_user_id),
                                 query_service: QueryHistoryService = Depends()):
    """
    Route to get the last record of second mode queries history.
    """
    return query_service.get_the_second_mode_query(user_id)


@router.get("/mode/third/one", response_model=ThirdModeQuery)
async def get_one_of_third_mode(*, user_id: int = Depends(get_current_user_id),
                                query_service: QueryHistoryService = Depends()):
    """
    Route to get the last record of third mode queries history.
    """
    return query_service.get_the_third_mode_query(user_id)


@router.get("/mode/first/all", response_model=List[FirstModeQueryInDatabase])
async def get_all_of_first_mode(*, user_id: int = Depends(get_current_user_id),
                                query_service: QueryHistoryService = Depends()):
    """
    Route to get all the records of first mode queries history.
    """
    return query_service.get_all_first_mode_queries(user_id)


@router.get("/mode/second/all", response_model=List[SecondModeQueryInDatabase])
async def get_all_of_second_mode(*, user_id: int = Depends(get_current_user_id),
                                 query_service: QueryHistoryService = Depends()):
    """
    Route to get all the records of second mode queries history.
    """
    return query_service.get_all_second_mode_queries(user_id)


@router.get("/mode/third/all", response_model=List[ThirdModeQueryInDatabase])
async def get_all_of_third_mode(*, user_id: int = Depends(get_current_user_id),
                                query_service: QueryHistoryService = Depends()):
    """
    Route to get all the records of third mode queries history.
    """
    return query_service.get_all_third_mode_queries(user_id)
