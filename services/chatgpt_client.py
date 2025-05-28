import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatGPTClient:
    def __init__(self, model="gpt-4"):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.model = model
        openai.api_key = OPENAI_API_KEY

    def generate_listing_info(self, product_context: str) -> dict:
        prompt = f"""
        Given this product description derived from image searches:

        {product_context}

        Generate the following:
        - A concise eCommerce title (max 80 characters)
        - A suggested price in USD
        - A bullet-point description
        - Suggested condition (new/used)
        - Suggested category tags

        Format the output as JSON.
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a product listing assistant for online marketplaces."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        return response.choices[0].message['content']