import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote

# Setup logger untuk module ini
logger = logging.getLogger(__name__)

class WhatsAppBot:
    def __init__(self, user_data_suffix=""):
        self.driver = None
        self.is_logged_in = False
        self.user_data_suffix = user_data_suffix
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome driver untuk WhatsApp Web dengan session persistent dan browser visible"""
        chrome_options = Options()
        
        # Buat folder untuk menyimpan session Chrome
        user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
        
        # Gunakan user data directory untuk menyimpan session
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument("--profile-directory=WhatsApp")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Cek apakah running dalam environment headless
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        # headless = False  # Set ke True untuk mode headless, False untuk mode visible

        if headless:
            # Mode headless untuk production/Docker
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--window-size=1920,1080")
            logger.info("🔧 Running in headless mode (Production/Docker environment)")
            print("🔧 Running in headless mode (Production/Docker environment)")
        else:
            # Mode visible untuk development/testing
            chrome_options.add_argument("--start-maximized")  # Maximize window
            chrome_options.add_argument("--window-size=1920,1080")  # Set window size
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Tambahan untuk debugging
            chrome_options.add_argument("--enable-logging")
            chrome_options.add_argument("--v=1")
            
            logger.info("🔧 Running in visible mode (Development/Testing environment)")
            print("🔧 Running in visible mode (Development/Testing environment)")

        try:
            # Membuka Chrome dengan driver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            if not headless:
                # Maximize window dan focus
                self.driver.maximize_window()
                time.sleep(1)  # Give time for window to maximize
                
            logger.info(f"✅ Chrome driver berhasil diinisialisasi dengan user data: {user_data_dir}")
            print(f"✅ Chrome driver berhasil diinisialisasi dengan user data: {user_data_dir}")
            print(f"🌐 Browser window {'visible' if not headless else 'headless'}")
            
            return self.driver
        except Exception as e:
            logger.error(f"❌ Gagal membuka Chrome: {e}")
            print(f"❌ Gagal membuka Chrome: {e}")
            self.driver = None
            return None

    def check_login_status(self):
        """Cek apakah WhatsApp sudah login dengan debugging visual"""
        if not self.driver:
            return False
            
        try:
            # Cek apakah ada elemen QR code (indikator belum login)
            qr_element = self.driver.find_element(By.XPATH, '//div[@data-testid="qr-code"]')
            if qr_element and qr_element.is_displayed():
                logger.info("❌ Belum login. QR Code terdeteksi.")
                print("❌ Belum login. QR Code terdeteksi.")
                print("📱 Silakan scan QR code dengan aplikasi WhatsApp di smartphone Anda")
                self.is_logged_in = False
                return False
        except:
            pass  # QR code tidak ditemukan, lanjutkan pengecekan
        
        # Multiple selectors untuk deteksi login yang lebih robust
        login_selectors = [
            # Search box
            '//div[@contenteditable="true"][@data-tab="3"]',
            '//div[@contenteditable="true"][contains(@class, "selectable-text")]',
            
            # Chat list / pane side
            '//div[@id="pane-side"]',
            '//div[contains(@class, "pane-side")]',
            
            # Header dengan menu
            '//header[contains(@class, "header")]',
            '//div[@data-testid="chatlist-header"]',
            
            # Kontainer chat list
            '//div[contains(@class, "chat-list")]',
            '//div[@data-testid="chat-list"]',
            
            # Main container setelah login
            '//div[@id="main"]',
            '//div[contains(@class, "two")]',
            
            # Menu button (3 dots)
            '//div[@data-testid="menu"]',
            '//span[@data-testid="menu"]',
            
            # Profile photo area
            '//div[contains(@class, "avatar")]',
            
            # Any contenteditable in main area
            '//div[@contenteditable="true"]'
        ]
        
        for selector in login_selectors:
            try:
                login_element = self.driver.find_element(By.XPATH, selector)
                if login_element and login_element.is_displayed():
                    logger.info(f"✅ Sudah login! (Detected by: {selector})")
                    print(f"✅ Sudah login! (Detected by: {selector})")
                    self.is_logged_in = True
                    return True
            except:
                continue
        
        # Cek dengan WebDriverWait untuk elemen yang mungkin loading
        try:
            WebDriverWait(self.driver, 5).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')),
                    EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]')),
                    EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chatlist-header"]'))
                )
            )
            logger.info("✅ Sudah login! (Detected by WebDriverWait)")
            print("✅ Sudah login! (Detected by WebDriverWait)")
            self.is_logged_in = True
            return True
        except:
            pass
        
        # Cek berdasarkan URL
        current_url = self.driver.current_url
        if "web.whatsapp.com" in current_url and "qr" not in current_url.lower():
            logger.info("✅ Sudah login! (Detected by URL pattern)")
            print("✅ Sudah login! (Detected by URL pattern)")
            self.is_logged_in = True
            return True
        
        logger.info("❌ Tidak dapat menemukan elemen login, kemungkinan tidak login.")
        print("❌ Tidak dapat menemukan elemen login, kemungkinan tidak login.")
        print("🔍 Current URL:", current_url)
        self.is_logged_in = False
        return False

    def wait_for_login(self, max_wait_time=60):
        """Tunggu hingga user login dengan feedback visual"""
        logger.info("⏳ Menunggu login...")
        print("⏳ Menunggu login...")
        print("📱 Silakan scan QR code jika muncul...")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            if self.check_login_status():
                print("🎉 Login berhasil terdeteksi!")
                return True
            
            remaining_time = int(max_wait_time - (time.time() - start_time))
            print(f"⏰ Menunggu login... ({remaining_time}s tersisa)", end='\r')
            time.sleep(2)  # Cek setiap 2 detik
        
        print("\n⏰ Timeout menunggu login!")
        return False

    def login(self):
        """Login ke WhatsApp Web dengan visual feedback"""
        if not self.driver:
            logger.error("❌ Chrome driver tidak tersedia")
            print("❌ Chrome driver tidak tersedia")
            return False
            
        try:
            logger.info("🚀 Membuka WhatsApp Web...")
            print("🚀 Membuka WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Tunggu halaman load
            headless = os.getenv("HEADLESS", "false").lower() == "true"
            wait_time = 10 if headless else 8
            
            logger.info(f"⏳ Menunggu halaman load ({wait_time} detik)...")
            print(f"⏳ Menunggu halaman load ({wait_time} detik)...")
            
            for i in range(wait_time):
                print(f"⏳ Loading... {i+1}/{wait_time}", end='\r')
                time.sleep(1)
            print("")  # New line
            
            # Tunggu sampai halaman benar-benar load
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, '//div[@data-testid="qr-code"]')),
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')),
                        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
                    )
                )
                logger.info("✅ Halaman WhatsApp Web berhasil dimuat")
                print("✅ Halaman WhatsApp Web berhasil dimuat")
            except:
                logger.warning("⚠️ Timeout menunggu halaman load, melanjutkan...")
                print("⚠️ Timeout menunggu halaman load, melanjutkan...")
            
            # Cek apakah sudah login dari session sebelumnya
            if self.check_login_status():
                logger.info("🎉 WhatsApp Web siap digunakan! (Login dari session sebelumnya)")
                print("🎉 WhatsApp Web siap digunakan! (Login dari session sebelumnya)")
                return True
            else:
                if headless:
                    logger.warning("🌐 Perlu scan QR Code untuk login (running in headless mode)")
                    print("🌐 Perlu scan QR Code untuk login (running in headless mode)")
                    
                    # Dalam headless mode, tunggu sebentar lagi untuk memastikan
                    logger.info("⏳ Tunggu tambahan 10 detik untuk memastikan...")
                    print("⏳ Tunggu tambahan 10 detik untuk memastikan...")
                    time.sleep(10)
                    
                    # Cek sekali lagi
                    if self.check_login_status():
                        logger.info("🎉 Login terdeteksi setelah waiting!")
                        print("🎉 Login terdeteksi setelah waiting!")
                        return True
                    
                    return False
                else:
                    print("🌐 Silakan scan QR Code untuk login.")
                    print("📱 Buka aplikasi WhatsApp di smartphone -> Menu (3 titik) -> Perangkat Tertaut -> Tautkan Perangkat")
                    
                    if self.wait_for_login(max_wait_time=120):  # Tunggu maksimal 2 menit
                        logger.info("🎉 Login berhasil! Session akan disimpan untuk penggunaan selanjutnya.")
                        print("🎉 Login berhasil! Session akan disimpan untuk penggunaan selanjutnya.")
                        return True
                    else:
                        logger.warning("⏰ Timeout! Anda tidak login dalam waktu yang ditentukan.")
                        print("⏰ Timeout! Anda tidak login dalam waktu yang ditentukan.")
                        return False
            
        except Exception as e:
            logger.error(f"❌ Login gagal: {e}")
            print(f"❌ Login gagal: {e}")
            return False

    def debug_page_elements(self):
        """Debug function untuk melihat elemen yang ada di halaman dengan visual feedback"""
        try:
            logger.info("🔍 Debugging elemen halaman...")
            print("🔍 Debugging elemen halaman...")
            
            # Print current URL
            current_url = self.driver.current_url if self.driver else "No driver"
            logger.info(f"Current URL: {current_url}")
            print(f"📍 Current URL: {current_url}")
            
            # Print page title
            page_title = self.driver.title if self.driver else "No title"
            logger.info(f"Page title: {page_title}")
            print(f"📄 Page title: {page_title}")
            
            # Print window size
            window_size = self.driver.get_window_size()
            print(f"🖥️  Window size: {window_size['width']}x{window_size['height']}")
            
            # Cek beberapa elemen penting
            elements_to_check = [
                ('Message Box (contenteditable)', '//div[@contenteditable="true"]'),
                ('Send Button (data-icon)', '//span[@data-icon="send"]'),
                ('Send Button (wds-ic-send)', '//span[contains(@class, "wds-ic-send")]'),
                ('Send Button (wds-ic-send-filled)', '//span[contains(@class, "wds-ic-send-filled")]'),
                ('Send Button (any wds-ic-send)', '//*[contains(@class, "wds-ic-send")]'),
                ('Send Button (aria-label)', '//button[contains(@aria-label, "Send")]'),
                ('Main Container', '//div[@id="main"]'),
                ('Compose Box', '//div[@data-testid="conversation-compose-box-input"]'),
                ('Footer', '//footer'),
                ('Compose Area', '//div[contains(@class, "compose-box")]')
            ]
            
            print("\n📋 Element Check Results:")
            print("-" * 60)
            
            for description, xpath in elements_to_check:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    status = f"✅ {len(elements)} found" if elements else "❌ Not found"
                    logger.info(f"{description}: {len(elements)} elements")
                    print(f"{description:30} | {status}")
                    
                    # Check if elements are visible
                    if elements:
                        visible_count = sum(1 for el in elements if el.is_displayed())
                        if visible_count > 0:
                            print(f"{' '*30} | 👁️  {visible_count} visible")
                        
                except Exception as e:
                    logger.info(f"Error checking {description}: {e}")
                    print(f"{description:30} | ❌ Error: {str(e)[:30]}...")
            
            print("-" * 60)
                    
        except Exception as e:
            logger.error(f"Debug error: {e}")
            print(f"❌ Debug error: {e}")

    def send_message(self, phone_number, message):
        """Kirim pesan teks ke nomor WhatsApp dengan visual feedback"""
        logger.info(f"🔍 send_message called - Phone: {phone_number}, Message: '{message}'")
        print(f"🔍 Starting send_message - Phone: {phone_number}, Message: '{message}'")
        
        if not self.driver:
            error_msg = "Chrome driver tidak tersedia"
            logger.error(f"❌ {error_msg}")
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
        
        if not self.check_login_status():
            error_msg = "Belum login ke WhatsApp Web"
            logger.error(f"❌ {error_msg}")
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
            
        try:
            # Format nomor telepon
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number.replace(' ', '').replace('-', '')
            
            logger.info(f"📞 Formatted phone number: {phone_number}")
            print(f"📞 Using phone number: {phone_number}")
            
            # Encode pesan untuk URL
            encoded_message = quote(message)
            
            # Buka chat dengan nomor tertentu
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
            logger.info(f"🌐 Opening URL: {url}")
            print(f"🌐 Navigating to chat URL...")
            
            self.driver.get(url)
            
            # Tunggu halaman load dengan visual feedback
            logger.info("⏳ Waiting for page load...")
            print("⏳ Waiting for chat page to load...")
            
            for i in range(8):
                print(f"⏳ Loading chat... {i+1}/8", end='\r')
                time.sleep(1)
            print("")  # New line
            
            # Debug elemen halaman
            logger.info("🔍 Starting page debug...")
            print("🔍 Debugging page elements...")
            self.debug_page_elements()
            
            # Cek apakah ada pesan error (nomor tidak valid)
            logger.info("🔍 Checking for error messages...")
            print("🔍 Checking for invalid phone number...")
            try:
                error_selectors = [
                    '//div[contains(text(), "Phone number shared via url is invalid")]',
                    '//div[contains(text(), "Nomor telepon")]',
                    '//div[contains(text(), "invalid")]'
                ]
                
                for error_selector in error_selectors:
                    try:
                        error_element = self.driver.find_element(By.XPATH, error_selector)
                        if error_element.is_displayed():
                            error_msg = f"Nomor telepon {phone_number} tidak valid"
                            logger.error(f"❌ {error_msg}")
                            print(f"❌ {error_msg}")
                            return {"status": "error", "message": error_msg}
                    except:
                        continue
            except Exception as e:
                logger.warning(f"⚠️ Error checking for error messages: {e}")
                print(f"⚠️ Could not check for error messages: {e}")
            
            # Metode 1: Cari dan isi textbox terlebih dahulu
            logger.info("🔍 Looking for message box...")
            print("🔍 Step 1: Looking for message input box...")
            
            message_box_selectors = [
                '//div[@contenteditable="true"][@data-tab="10"]',
                '//div[@contenteditable="true"][@data-tab="1"]',
                '//div[@data-testid="conversation-compose-box-input"]',
                '//div[@contenteditable="true"][contains(@class, "selectable-text")]',
                '//div[@contenteditable="true"][contains(@title, "Type a message")]',
                '//div[@contenteditable="true"]',
                'div[contenteditable="true"]',
                '[contenteditable="true"]'
            ]
            
            message_box = None
            for i, selector in enumerate(message_box_selectors):
                try:
                    logger.info(f"🔍 Trying message box selector {i+1}/{len(message_box_selectors)}: {selector}")
                    print(f"   Trying selector {i+1}/{len(message_box_selectors)}: {selector[:50]}...")
                    
                    if selector.startswith('//'):
                        message_box = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        message_box = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    if message_box and message_box.is_displayed():
                        logger.info(f"✅ Message box found with selector: {selector}")
                        print(f"✅ Found message box with selector {i+1}")
                        break
                except Exception as e:
                    logger.info(f"⚠️ Message box selector {selector} failed: {e}")
                    print(f"   ❌ Selector {i+1} failed")
                    continue
            
            if message_box:
                try:
                    logger.info("📝 Typing message...")
                    print("📝 Step 2: Typing message into input box...")
                    
                    # Clear existing text dan input pesan baru
                    message_box.clear()
                    message_box.click()
                    time.sleep(1)
                    message_box.send_keys(message)
                    time.sleep(2)
                    
                    logger.info(f"✅ Message '{message}' typed successfully")
                    print(f"✅ Message typed successfully: '{message}'")
                    
                    # Tunggu sebentar agar icon berubah menjadi wds-ic-send-filled
                    print("⏳ Waiting for send button to become active...")
                    time.sleep(2)
                    
                    # Metode 2: Coba kirim dengan Enter key terlebih dahulu
                    try:
                        logger.info("⌨️ Trying to send with Enter key...")
                        print("⌨️ Step 3a: Trying to send with Enter key...")
                        
                        message_box.send_keys(Keys.ENTER)
                        time.sleep(3)
                        
                        logger.info("✅ Message sent with Enter key")
                        print("✅ Message sent successfully with Enter key!")
                        return {"status": "success", "message": "Pesan berhasil dikirim (Enter key)"}
                    except Exception as e:
                        logger.info(f"⚠️ Enter key failed: {e}, trying send button...")
                        print(f"⚠️ Enter key failed, trying send button...")
                        pass
                        
                except Exception as e:
                    logger.error(f"❌ Failed to type message: {e}")
                    print(f"❌ Failed to type message: {e}")
            else:
                logger.warning("⚠️ Message box not found, looking for send button directly")
                print("⚠️ Message box not found, looking for send button directly")
            
            # Metode 3: Tunggu dan klik tombol send dengan selector terbaru
            logger.info("🔍 Looking for send button...")
            print("🔍 Step 3b: Looking for send button...")
            
            send_selectors = [
                # Selector terbaru dengan wds-ic-send-filled
                '//span[contains(@class, "wds-ic-send-filled")]',
                '//*[contains(@class, "wds-ic-send-filled")]',
                '//button[.//span[contains(@class, "wds-ic-send-filled")]]',
                '//div[.//span[contains(@class, "wds-ic-send-filled")]]',
                
                # Selector lama yang masih mungkin aktif
                '//span[@data-icon="send"]',
                '//span[contains(@class, "wds-ic-send")]',
                '//*[contains(@class, "wds-ic-send")]',
                
                # Selector baru yang ditambahkan
                '//span[contains(@class, "wds-ic-send")]//following-sibling::*[@aria-label="Send"]',
                '//button[@aria-label="Send"]',
                '//div[@aria-label="Send"]',
                
                # Selector generik
                '//span[@data-testid="send"]',
                '//button[contains(@class, "send")]',
                '//div[contains(@class, "send")]',
                '//span[contains(@class, "send")]',
                '//*[@data-icon="send"]',
                '//button[contains(text(), "Send")]',
                '//div[contains(text(), "Send")]',
                
                # Kombinasi dengan aria-label untuk button dan div
                '//*[@aria-label="Send" or @aria-label="Kirim"]',
                '//button[contains(@aria-label, "Send")]',
                '//div[contains(@aria-label, "Send")]'
            ]
            
            sent = False
            for i, selector in enumerate(send_selectors):
                try:
                    logger.info(f"🔍 Trying send button selector {i+1}/{len(send_selectors)}: {selector}")
                    print(f"   Trying send button {i+1}/{len(send_selectors)}...")
                    
                    send_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    
                    if send_button and send_button.is_displayed():
                        send_button.click()
                        logger.info(f"✅ Message sent to {phone_number} with selector: {selector}")
                        print(f"✅ Message sent successfully with send button {i+1}!")
                        time.sleep(2)
                        sent = True
                        break
                        
                except Exception as e:
                    logger.info(f"⚠️ Send button selector {selector} failed: {e}")
                    print(f"   ❌ Send button {i+1} failed")
                    continue
            
            if sent:
                return {"status": "success", "message": "Pesan berhasil dikirim"}
            else:
                # Metode 4: Fallback dengan JavaScript yang diperbaiki
                try:
                    logger.info("🔧 Trying JavaScript fallback...")
                    print("🔧 Step 4: Trying JavaScript fallback...")
                    
                    js_script = """
                    // Cari tombol send dengan class dan aria-label terbaru
                    var sendButton = document.querySelector('.wds-ic-send-filled') ||
                                   document.querySelector('.wds-ic-send') ||
                                   document.querySelector('[data-icon="send"]') ||
                                   document.querySelector('[aria-label*="Send"]') ||
                                   document.querySelector('[aria-label*="Kirim"]') ||
                                   document.querySelector('button[aria-label*="Send"]') ||
                                   document.querySelector('div[aria-label*="Send"]') ||
                                   document.querySelector('span[data-icon="send"]');
                    
                    if (sendButton) {
                        // Jika elemen adalah icon, cari parent button/div yang clickable
                        var clickableParent = sendButton.closest('button') || 
                                            sendButton.closest('div[role="button"]') || 
                                            sendButton.closest('div[aria-label*="Send"]') ||
                                            sendButton;
                        clickableParent.click();
                        return 'success';
                    }
                    return 'not_found';
                    """
                    
                    result = self.driver.execute_script(js_script)
                    
                    if result == 'success':
                        logger.info("✅ Message sent with JavaScript")
                        print("✅ Message sent successfully with JavaScript!")
                        return {"status": "success", "message": "Pesan berhasil dikirim (JavaScript)"}
                    else:
                        logger.error("❌ Send button not found with JavaScript")
                        print("❌ Send button not found with JavaScript")
                        
                except Exception as e:
                    logger.error(f"❌ JavaScript fallback failed: {e}")
                    print(f"❌ JavaScript fallback failed: {e}")
                
                error_msg = "Tidak dapat menemukan tombol send setelah semua percobaan"
                logger.error(f"❌ {error_msg}")
                print(f"❌ {error_msg}")
                print("💡 Coba check manual di browser yang terbuka")
                return {"status": "error", "message": error_msg}
            
        except Exception as e:
            error_msg = f"Exception in send_message: {str(e)}"
            logger.error(f"❌ {error_msg}")
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}

    def send_media(self, phone_number, media_path, caption=""):
        """Kirim file media dengan caption"""
        if not self.driver:
            return {"status": "error", "message": "Chrome driver tidak tersedia"}
        
        if not self.check_login_status():
            return {"status": "error", "message": "Belum login ke WhatsApp Web"}
        
        if not os.path.exists(media_path):
            return {"status": "error", "message": f"File tidak ditemukan: {media_path}"}
            
        try:
            # Format nomor telepon
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number.replace(' ', '').replace('-', '')
            
            # Buka chat dengan nomor tertentu
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            logger.info(f"📞 Membuka chat dengan {phone_number}")
            self.driver.get(url)
            
            time.sleep(3)
            
            # Klik tombol attachment
            attachment_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]'))
            )
            attachment_button.click()
            
            time.sleep(1)
            
            # Klik "Photos & Videos" atau "Document"
            file_selectors = [
                '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]',
                '//input[@accept="*"]'
            ]
            
            file_input = None
            for selector in file_selectors:
                try:
                    file_input = self.driver.find_element(By.XPATH, selector)
                    break
                except:
                    continue
            
            if not file_input:
                return {"status": "error", "message": "Tidak dapat menemukan input file"}
            
            # Upload file
            file_input.send_keys(os.path.abspath(media_path))
            time.sleep(2)
            
            # Tambahkan caption jika ada
            if caption:
                try:
                    caption_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                    caption_box.send_keys(caption)
                except:
                    pass  # Caption optional
            
            # Klik tombol send dengan selector terbaru yang diperbaiki
            send_selectors = [
                '//span[contains(@class, "wds-ic-send-filled")]',
                '//span[@data-icon="send"]',
                '//*[contains(@class, "wds-ic-send")]',
                '//button[@aria-label="Send"]',
                '//div[@aria-label="Send"]',
                '//*[@aria-label="Send" or @aria-label="Kirim"]',
                '//button[contains(@aria-label, "Send")]',
                '//div[contains(@aria-label, "Send")]'
            ]
            
            sent = False
            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    send_button.click()
                    sent = True
                    break
                except:
                    continue
            
            if sent:
                logger.info(f"✅ Media berhasil dikirim ke {phone_number}")
                return {"status": "success", "message": "Media berhasil dikirim"}
            else:
                return {"status": "error", "message": "Tidak dapat menemukan tombol send untuk media"}
            
        except Exception as e:
            logger.error(f"❌ Gagal mengirim media: {e}")
            return {"status": "error", "message": str(e)}

    def get_qr_code_status(self):
        """Cek status QR code"""
        if not self.driver:
            return "driver_not_available"
        
        try:
            # Cek apakah ada QR code
            qr_element = self.driver.find_element(By.XPATH, '//div[@data-testid="qr-code"]')
            if qr_element and qr_element.is_displayed():
                return "qr_visible"
        except:
            pass
        
        try:
            # Cek apakah sudah login
            login_element = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            if login_element.is_displayed():
                return "logged_in"
        except:
            pass
        
        return "unknown"
    
    def close(self):
        """Tutup browser"""
        if self.driver:
            logger.info("🔒 Menutup browser...")
            print("🔒 Menutup browser...")
            self.driver.quit()

# Fungsi helper untuk testing
def test_bot():
    """Test function untuk coba bot"""
    print("🧪 Testing WhatsApp Bot...")
    
    bot = WhatsAppBot()
    
    if not bot.driver:
        print("❌ Tidak dapat membuka WhatsApp Web")
        return
    
    try:
        # Login
        if bot.login():
            print("🎉 WhatsApp Web siap digunakan!")
            
            # Test kirim pesan
            phone = input("Masukkan nomor HP (dengan kode negara, contoh: +628123456789): ")
            message = input("Masukkan pesan: ")
            
            result = bot.send_message(phone, message)
            print(f"Hasil: {result}")
        else:
            print("🔴 Anda belum login. Mohon lakukan login terlebih dahulu.")
        
        # Biarkan browser terbuka setelah pengecekan
        input("Tekan Enter untuk keluar...")
        
    finally:
        bot.close()

if __name__ == "__main__":
    test_bot()