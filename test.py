import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = r"chromedriver"

def initialize_driver():
    """Initialize a stealth Chrome WebDriver."""
    print("[INFO] Initializing Chrome WebDriver in headless mode...")

    options = uc.ChromeOptions()
    options.add_argument("--headless")  # Fully headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        print("[SUCCESS] WebDriver initialized successfully!")
        return driver
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        return None
        
def get_video_and_subtitles(url):
    """Extracts video source URL and subtitle URLs from the page and saves them to d.json and index.html."""
    print(f"[INFO] Opening URL: {url}")
    driver = initialize_driver()
    
    if not driver:
        print("[ERROR] WebDriver not initialized. Exiting...")
        return

    driver.get(url)
    print("[INFO] Waiting for the page to load...")
    time.sleep(5)  # Wait for the page to load

    video_source = None
    subtitle_tracks = []

    try:
        # Save the page source as index.html
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print("[SUCCESS] Page saved as index.html.")
        print(30*"--")
        print(driver.page_source)
        print(30*"--")
        
        # Find the video element
        print("[INFO] Searching for video element...")
        video_element = driver.find_element(By.CSS_SELECTOR, 'video[preload="metadata"]')

        # Get video source URL
        video_source = video_element.find_element(By.TAG_NAME, "source").get_attribute("src")
        if video_source:
            print(f"[SUCCESS] Extracted Video URL: {video_source}")
        else:
            print("[WARNING] No video source URL found!")

        # Get subtitle tracks
        print("[INFO] Searching for subtitle tracks...")
        track_elements = video_element.find_elements(By.TAG_NAME, "track")
        for track in track_elements:
            subtitle_url = track.get_attribute("src")
            if subtitle_url:
                subtitle_tracks.append(subtitle_url)

        if subtitle_tracks:
            print(f"[SUCCESS] Extracted {len(subtitle_tracks)} subtitle track(s).")
        else:
            print("[WARNING] No subtitles found!")

        # Save data to JSON file
        data = {"url": video_source, "subtitles": subtitle_tracks}
        # with open("d.json", "w", encoding="utf-8") as json_file:
        #     json.dump(data, json_file, indent=4)
        print("[SUCCESS] Data saved to d.json!")

    except Exception as e:
        print(f"[ERROR] Failed to extract video/subtitles: {e}")

    finally:
        print("[INFO] Closing WebDriver...")
        driver.quit()
        print("[INFO] WebDriver closed.")




# Example usage
url = "https://www.miruro.tv/watch?id=176496&ep=2"
get_video_and_subtitles(url)
