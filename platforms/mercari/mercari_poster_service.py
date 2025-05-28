from botasaurus_driver import Driver
from automation import bot_driver_pool
from typing import List

class MercariPosterService:
    def __init__(self, title: str, price: float, description: str, image_paths: List[str]):
        self.title = title
        self.price = price
        self.description = description
        self.image_paths = image_paths
        self.bot: Driver = None

    def post_item(self) -> dict:
        self.bot = bot_driver_pool.get_driver_from_pool()
        if not self.bot:
            return {"success": False, "message": "No available drivers."}

        try:
            self.bot.get("https://www.mercari.com/sell")
            self.bot.sleep(3)

            self.bot.type("input[name='name']", self.title)
            self.bot.type("textarea[name='description']", self.description)
            self.bot.type("input[name='price']", str(self.price))

            file_input = self.bot.query_selector("input[type='file']")
            if file_input:
                for path in self.image_paths:
                    file_input.upload_file(path)

            self.bot.click("button[type='submit']")
            self.bot.sleep(5)

            return {"success": True, "message": "Item posted to Mercari."}

        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}

        finally:
            bot_driver_pool.release_driver_to_pool(self.bot)