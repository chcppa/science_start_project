from asyncio import get_event_loop

from paralleldots import (
    config,
    sentiment,
    emotion,
    taxonomy,
    abuse
)

from services.text_analysis.models import (
    SentimentAnalysisResponse,
    ClassificationAnalysisResponse,
    EmotionAnalysisResponse,
    AbuseAnalysisResponse,
    TextRequest,
    FirstModeResponse,
    SecondModeResponse,
    ThirdModeResponse
)

from settings import settings

config.set_api_key(settings.paralleldots_api_key)  # check "set_api_key" implementation to edit path to *.cfg


class TextAnalysisService:

    def __init__(self, text: str):
        self.text = TextRequest(text=text)

    @staticmethod
    def get_the_most_important_fields(analysis_result: dict[str, float], num_of_fields: int) -> dict[str, float]:
        """
        Return the highest fields by value
        """
        sorted_data: list = sorted(
            analysis_result.items(),
            key=lambda item: item[1],
            reverse=True
        )[0:num_of_fields]

        return dict(sorted_data)

    @staticmethod
    def round_dict_values(data: dict[str, float]) -> dict[str, int]:
        """
        Convert values to percents.
        """

        return dict(zip(data.keys(), map(lambda x: int(round(x * 100)), data.values())))

    @classmethod
    def parse_the_main_text_subject(cls,
                                    analysis_result: list[dict[str, str | float]]) -> ClassificationAnalysisResponse:
        """
        Get the highest subject from some percentages.
        """
        subject = sorted(analysis_result, key=lambda x: x["confidence_score"], reverse=True)[0]
        subject["confidence_score"] = int(round(subject["confidence_score"] * 100))

        return ClassificationAnalysisResponse(**subject)

    def sentiment_analyse(self) -> SentimentAnalysisResponse:
        result: dict[str, int] = self.round_dict_values(sentiment(self.text.text)["sentiment"])

        return SentimentAnalysisResponse(**result)

    def classificate(self) -> ClassificationAnalysisResponse:
        analysis_result: list[dict[str, str | float]] = taxonomy(self.text.text)["taxonomy"]

        subject = self.parse_the_main_text_subject(analysis_result)

        return subject

    def emotion_analysis(self) -> EmotionAnalysisResponse:
        analysis_result: dict[str, float] = emotion(self.text.text)["emotion"]
        parsed_result: dict[str, int] = self.round_dict_values(
            self.get_the_most_important_fields(
                analysis_result=analysis_result,
                num_of_fields=3
            )
        )

        return EmotionAnalysisResponse(**parsed_result)

    def abuse_analysis(self) -> AbuseAnalysisResponse:
        analysis_result: dict[str, float] = abuse(self.text.text)
        parsed_result: dict[str, int] = self.round_dict_values(analysis_result)

        return AbuseAnalysisResponse(**parsed_result)

    async def analyse_by_first_mode(self) -> FirstModeResponse:
        loop = get_event_loop()

        return FirstModeResponse(
            classification_result=await loop.run_in_executor(
                None, self.classificate))

    async def analyse_by_second_mode(self) -> SecondModeResponse:
        loop = get_event_loop()

        return SecondModeResponse(
            sentiment_analysis_result=await loop.run_in_executor(
                None, self.sentiment_analyse),
            emotion_analysis_result=await loop.run_in_executor(
                None, self.emotion_analysis)
        )

    async def analyse_by_third_mode(self) -> ThirdModeResponse:
        loop = get_event_loop()

        return ThirdModeResponse(
            emotion_analysis_result=await loop.run_in_executor(
                None, self.emotion_analysis),
            abuse_analysis_result=await loop.run_in_executor(
                None, self.abuse_analysis)
        )
