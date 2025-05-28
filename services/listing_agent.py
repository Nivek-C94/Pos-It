from services.image_search import reverse_image_search
from services.chatgpt_client import ChatGPTClient
from platforms.ebay.ebay_poster_service import PosterService as EbayPoster
from platforms.mercari.mercari_poster_service import MercariPosterService
import tempfile
import shutil
import os

def process_image_and_generate_listing(image_path: str) -> dict:
    context = reverse_image_search(image_path)
    gpt = ChatGPTClient()
    listing_json = gpt.generate_listing_info(context)
    return listing_json

def post_listing_to_all(listing_data: dict, image_paths: list) -> dict:
    results = {}

    # eBay
    try:
        from models.post_item_models import PostItemRequest, PostItemResponse
        req = PostItemRequest(
            title=listing_data.get("title"),
            price=float(listing_data.get("price", 0)),
            sku="AUTO-GEN",
            condition=listing_data.get("condition", "used"),
            specifics=listing_data.get("tags", {}),
            shipping_info=None,
            return_policy=None,
            image_urls=[]  # not used, we pass image_paths
        )
        ebay = EbayPoster(req, raw_request={})
        ebay.local_image_paths = image_paths
        results['ebay'] = ebay.post_item().dict()
    except Exception as e:
        results['ebay'] = {"success": False, "error": str(e)}

    # Mercari
    try:
        mercari = MercariPosterService(
            title=listing_data.get("title"),
            price=float(listing_data.get("price", 0)),
            description=listing_data.get("description"),
            image_paths=image_paths
        )
        results['mercari'] = mercari.post_item()
    except Exception as e:
        results['mercari'] = {"success": False, "error": str(e)}

    return results