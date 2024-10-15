# tweet_scraper.py

from playwright.sync_api import sync_playwright
from typing import Dict
import jmespath

def scrape_tweet(url: str) -> Dict:
    _xhr_calls = []
    def intercept_response(response):
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.on("response", intercept_response)
        page.goto(url)
        page.wait_for_selector("[data-testid='tweet']")
        tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
        if tweet_calls:
            for xhr in tweet_calls:
                try:
                    data = xhr.json()
                    return data['data']['tweetResult']['result']
                except Exception as e:
                    print(f"Error parsing XHR response: {e}")
        else:
            print("No relevant XHR calls found.")
        return {}

def parse_user(user_data: Dict) -> Dict:
    return {
        "user_id": user_data.get("rest_id"),
        "name": jmespath.search("legacy.name", user_data),
        "screen_name": jmespath.search("legacy.screen_name", user_data),
        "description": jmespath.search("legacy.description", user_data),
        "followers_count": jmespath.search("legacy.followers_count", user_data),
        "following_count": jmespath.search("legacy.friends_count", user_data),
        "statuses_count": jmespath.search("legacy.statuses_count", user_data),
        "verified": jmespath.search("legacy.verified", user_data),
        "profile_image_url": jmespath.search("legacy.profile_image_url_https", user_data),
        "created_at": jmespath.search("legacy.created_at", user_data),
    }

def parse_tweet(data: Dict) -> Dict:
    result = jmespath.search(
        """{
        created_at: legacy.created_at,
        attached_urls: legacy.entities.urls[].expanded_url,
        attached_media: legacy.entities.media[].media_url_https,
        tagged_users: legacy.entities.user_mentions[].screen_name,
        tagged_hashtags: legacy.entities.hashtags[].text,
        favorite_count: legacy.favorite_count,
        reply_count: legacy.reply_count,
        retweet_count: legacy.retweet_count,
        text: legacy.full_text,
        is_quote: legacy.is_quote_status,
        is_retweet: legacy.retweeted,
        language: legacy.lang,
        user_id: legacy.user_id_str,
        id: legacy.id_str,
        conversation_id: legacy.conversation_id_str
    }""", data)

    user_data = jmespath.search("core.user_results.result", data)
    if user_data:
        result["user"] = parse_user(user_data)

    return result
