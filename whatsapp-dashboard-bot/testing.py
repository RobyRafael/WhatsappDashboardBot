import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """Setup Chrome driver untuk WhatsApp Web dengan session persistent"""
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
    chrome_options.add_argument("--window-size=1200,800")

    try:
        # Membuka Chrome dengan driver
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Gagal membuka Chrome: {e}")
        return None

def check_login_status(driver):
    """Cek apakah WhatsApp sudah login menggunakan try-except"""
    try:
        # Cek apakah ada elemen QR code (indikator belum login)
        qr_element = driver.find_element(By.XPATH, '//div[@data-testid="qr-code"]')
        if qr_element and qr_element.is_displayed():
            print("❌ Belum login. Silakan scan QR Code.")
            return False
    except:
        pass  # QR code tidak ditemukan, lanjutkan pengecekan
    
    try:
        # Cek elemen lain yang menandakan bahwa pengguna sudah login
        login_element = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')  # Search box
        if login_element.is_displayed():
            print("✅ Sudah login!")
            return True
    except:
        pass
    
    try:
        # Cek elemen chat list sebagai indikator login
        chat_list = driver.find_element(By.XPATH, '//div[@id="pane-side"]')
        if chat_list.is_displayed():
            print("✅ Sudah login!")
            return True
    except:
        pass
    
    print("❌ Tidak dapat menemukan elemen login, kemungkinan tidak login.")
    return False

def wait_for_login(driver, max_wait_time=60):
    """Tunggu hingga user login dengan timeout"""
    print("⏳ Menunggu login...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        if check_login_status(driver):
            return True
        time.sleep(2)  # Cek setiap 2 detik
    
    return False

def open_whatsapp():
    """Buka WhatsApp Web dan cek login status"""
    driver = setup_driver()
    if driver:
        driver.get("https://web.whatsapp.com")
        
        # Tunggu halaman load
        time.sleep(5)
        
        # Cek apakah sudah login dari session sebelumnya
        if check_login_status(driver):
            print("🎉 WhatsApp Web siap digunakan! (Login dari session sebelumnya)")
        else:
            print("🌐 Silakan scan QR Code untuk login.")
            if wait_for_login(driver, max_wait_time=120):  # Tunggu maksimal 2 menit
                print("🎉 Login berhasil! Session akan disimpan untuk penggunaan selanjutnya.")
            else:
                print("⏰ Timeout! Anda tidak login dalam waktu yang ditentukan.")
        
        # Biarkan browser terbuka setelah pengecekan
        input("Tekan Enter untuk menutup browser...")
        driver.quit()
    else:
        print("❌ Tidak dapat membuka WhatsApp Web")

if __name__ == "__main__":
    open_whatsapp()
