import asyncio

from googletrans import Translator as Gtrans

from services.text_analysis.models import TranslateTextRequest


class TranslatorService:

    def __init__(self, text: TranslateTextRequest):
        self.translator = Gtrans()
        self.text = text

    async def text_to_english(self) -> str:
        """
        Translate text to English.
        """
        loop = asyncio.get_event_loop()
        translation = await loop.run_in_executor(None, self.translator.translate, self.text.text_to_translate, "en")

        return translation.text

    def text_to_russian(self):
        raise NotImplementedError
