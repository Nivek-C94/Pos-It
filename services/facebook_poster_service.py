from bot_driver_pool import get_driver
import time


def post_to_facebook(listing_data, image_paths):
    """
    Posts a product listing to Facebook Marketplace.

    Args:
        listing_data (dict): title, price, category, etc.
        image_paths (list[str]): list of image file paths

    Returns:
        str: status message or result
    """
    driver = get_driver("facebook")
    try:
        driver.get("https://www.facebook.com/marketplace/create/item")
        time.sleep(3)

        # Example stubs
        # Fill title
        title_input = driver.find_element("xpath", "//input[@aria-label='Title']")
        title_input.send_keys(listing_data.get("title", ""))

        # Upload first image only for now
        image_input = driver.find_element("xpath", "//input[@type='file']")
        image_input.send_keys("\n".join(image_paths))

        # Stub - fill additional fields, click post
        # ...

        return "Posted to Facebook Marketplace"
    except Exception as e:
        return f"Facebook post failed: {str(e)}"
    finally:
        driver.quit()