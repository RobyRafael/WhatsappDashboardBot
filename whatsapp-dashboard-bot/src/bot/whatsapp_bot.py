import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import uuid

class WhatsAppBot:
    def __init__(self, user_data_suffix=""):
        self.driver = None
        self.user_data_suffix = user_data_suffix
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver for WhatsApp Web using Selenium Manager"""
        chrome_options = Options()
        
        # Create unique user data directory for each instance
        user_data_dir = f"./User_Data_{self.user_data_suffix}" if self.user_data_suffix else "./User_Data"
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--remote-debugging-port={9222 + hash(self.user_data_suffix) % 1000}")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        
        # For headless mode in production
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        if headless:
            chrome_options.add_argument("--headless")
        
        # Use system Chrome binary
        chrome_options.binary_location = "/usr/bin/google-chrome"
        
        try:
            # Let Selenium Manager handle ChromeDriver automatically
            self.driver = webdriver.Chrome(options=chrome_options)
            logging.info(f"Chrome driver initialized successfully with Selenium Manager (User Data: {user_data_dir})")
        except Exception as e:
            logging.error(f"Failed to initialize Chrome driver with Selenium Manager: {e}")
            # Fallback: try with webdriver-manager
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logging.info(f"Chrome driver initialized successfully with WebDriverManager (User Data: {user_data_dir})")
            except Exception as e2:
                logging.error(f"Failed to initialize Chrome driver with WebDriverManager: {e2}")
                self.driver = None
        
    def login(self):
        """Login to WhatsApp Web"""
        if not self.driver:
            logging.error("Chrome driver not initialized")
            return False
            
        try:
            self.driver.get("https://web.whatsapp.com")
            print("Please scan the QR code to login...")  # ← QR code muncul di sini
            
            # Wait for login completion
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("Login successful!")
            return True
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False
    
    def send_message(self, phone_number, message):
        """Send text message to phone number"""
        if not self.driver:
            return {"status": "error", "message": "Chrome driver not initialized"}
            
        try:
            # Format phone number
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
                
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            self.driver.get(url)
            
            # Wait for message input
            message_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Send message
            send_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            
            time.sleep(2)
            return {"status": "success", "message": "Message sent successfully"}
            
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            return {"status": "error", "message": str(e)}
    
    def send_media(self, phone_number, media_path, caption=""):
        """Send media file with optional caption"""
        if not self.driver:
            return {"status": "error", "message": "Chrome driver not initialized"}
            
        try:
            # Navigate to chat
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
                
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            self.driver.get(url)
            
            # Click attachment button
            attachment_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]'))
            )
            attachment_btn.click()
            
            # Click on document/media option
            media_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
            )
            
            # Upload file
            media_btn.send_keys(os.path.abspath(media_path))
            
            # Add caption if provided
            if caption:
                caption_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                caption_input.send_keys(caption)
            
            # Send
            send_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_btn.click()
            
            time.sleep(3)
            return {"status": "success", "message": "Media sent successfully"}
            
        except Exception as e:
            logging.error(f"Failed to send media: {e}")
            return {"status": "error", "message": str(e)}
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()