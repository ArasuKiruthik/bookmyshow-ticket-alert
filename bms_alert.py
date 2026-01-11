WHATSAPP_NUMBER = "+919655266886X"
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pywhatkit

# 🎬 MOVIE PAGE
URL = "https://in.bookmyshow.com/movies/pondicherry/parasakthi/buytickets/ET00431398/20260110"

# 🔁 SAFE REFRESH TIME (seconds)
MIN_DELAY = 7
MAX_DELAY = 12

# ⏸ BLOCK PAUSE (10–15 minutes)
BLOCK_MIN = 600   # 10 min
BLOCK_MAX = 900   # 15 min

# 📱 WHATSAPP DETAILS (EDIT THIS)
WHATSAPP_NUMBER = "+91XXXXXXXXXX"
WHATSAPP_MESSAGE = "🎉 Parasakthi tickets are now OPEN on BookMyShow! Go book fast!"

# 🧠 CHROME OPTIONS (HEADLESS MODE)
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("🎬 BookMyShow Alert Bot Started (Headless Mode)...")
driver.get(URL)
time.sleep(5)


def is_blocked(page_text):
    block_words = [
        "access denied",
        "too many requests",
        "blocked",
        "captcha",
        "verify you are human",
        "unusual traffic"
    ]
    return any(word in page_text for word in block_words)


def booking_open(page_text):
    keywords = ["book", "available", "showtime", "tickets"]
    return any(word in page_text for word in keywords)


def auto_click_pvr():
    try:
        buttons = driver.find_elements(By.XPATH, "//button")
        for btn in buttons:
            if "book" in btn.text.lower():
                btn.click()
                print("🖱 Auto-clicked Book button!")
                return True
    except:
        pass
    return False


def send_whatsapp_alert():
    print("📱 Sending WhatsApp alert...")
    pywhatkit.sendwhatmsg_instantly(
        phone_no=WHATSAPP_NUMBER,
        message=WHATSAPP_MESSAGE,
        wait_time=10,
        tab_close=True
    )


while True:
    try:
        page_text = driver.page_source.lower()

        # 🚫 BLOCK DETECTION
        if is_blocked(page_text):
            pause_time = random.randint(BLOCK_MIN, BLOCK_MAX)
            print("\n🚫 BLOCK DETECTED!")
            print(f"⏸ Pausing for {pause_time // 60} minutes to stay safe...")
            os.system("say 'Warning. You may be blocked by BookMyShow. Pausing.'")
            time.sleep(pause_time)
            driver.refresh()
            continue

        # 🎉 BOOKING CHECK
        if booking_open(page_text):
            print("\n🚨 BOOKING IS OPEN! AUTO-ACTION TRIGGERED!")
            os.system("say 'Booking is now open for Parasakthi on BookMyShow'")

            auto_click_pvr()
            send_whatsapp_alert()

            print("✅ Alert sent successfully!")
            break

        # 🔁 SAFE REFRESH
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"❌ Not open yet... checking again in {delay} seconds.")
        time.sleep(delay)
        driver.refresh()

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(15)


