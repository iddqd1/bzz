from abc import ABC
from abc import abstractmethod

from google import genai


class BaseGeminiAnalyzer(ABC):
    """Gemini analyzer. It uses Google GenAI to analyze PDF content."""

    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, text: str, schema: str) -> str | None:
        data = text + schema
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",  # gemini-2.0-flash-lite  gemini-2.0-flash
            config={"response_mime_type": "application/json"},
            contents=data,
        )
        return response.text

    @abstractmethod
    def get_schema(self) -> str:
        """Get schema for the analyzer."""

    def start_analyze(self, text: str) -> str | None:
        schema = self.get_schema()
        return self.generate_content(text, schema)


class HoldingsGeminiAnalyzer(BaseGeminiAnalyzer):
    """Holdings Gemini analyzer."""

    def get_schema(self) -> str:
        return """Parse document. Return list of holdings.
        Set null for missing values.
        Position should be from 1 to n, where 1 is the biggest holding.
        Use this schema:
        [
        {
        "name": str,
        "percentage": float,
        "position": int,
        }]"""


class PriceGeminiAnalyzer(BaseGeminiAnalyzer):
    """Price Gemini analyzer."""

    def get_schema(self) -> str:
        return """Parse document. Return latest price of the instrument.
        Use this schema:
        {
        "date": str,
        "price": float,
        }"""


def get_gemini_analyzer(analyzer_type: str, api_key: str) -> BaseGeminiAnalyzer:
    if analyzer_type == "holdings":
        return HoldingsGeminiAnalyzer(api_key)
    if analyzer_type == "price":
        return PriceGeminiAnalyzer(api_key)

    msg = f"Unknown analyzer type: {analyzer_type}"
    raise ValueError(msg)
