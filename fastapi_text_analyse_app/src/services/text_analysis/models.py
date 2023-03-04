from pydantic import BaseModel, Field


class SentimentAnalysisResponse(BaseModel):
    negative: int
    neutral: int
    positive: int


class ClassificationAnalysisResponse(BaseModel):
    confidence_score: int
    tag: str


class EmotionAnalysisResponse(BaseModel):
    angry: int | None = Field(alias="Angry")
    sad: int | None = Field(alias="Sad")
    excited: int | None = Field(alias="Excited")
    bored: int | None = Field(alias="Bored")
    happy: int | None = Field(alias="Happy")
    fear: int | None = Field(alias="Fear")


class AbuseAnalysisResponse(BaseModel):
    abusive: int
    hate_speech: int
    neither: int


class TextRequest(BaseModel):
    """
    Text from request.
    """
    text: str = Field(
        max_length=40,
        description="Internal free-plan API has a limit, app in the test-mode right now."
    )


class TranslateTextRequest(BaseModel):
    text_to_translate: str = Field(max_length=14999, description="Internal API requires length not over 15K symbols")


class FirstModeResponse(BaseModel):
    classification_result: ClassificationAnalysisResponse


class SecondModeResponse(BaseModel):
    sentiment_analysis_result: SentimentAnalysisResponse
    emotion_analysis_result: EmotionAnalysisResponse


class ThirdModeResponse(BaseModel):
    emotion_analysis_result: EmotionAnalysisResponse
    abuse_analysis_result: AbuseAnalysisResponse
