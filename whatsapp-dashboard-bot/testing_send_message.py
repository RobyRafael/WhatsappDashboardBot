import sys
import os

# Add src to path dengan path yang lebih absolut
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

print(f"Current directory: {current_dir}")
print(f"Source path: {src_path}")
print(f"Python path: {sys.path[:3]}")  # Show first 3 paths

try:
    from bot.whatsapp_bot import WhatsAppBot
    print("✅ Import berhasil!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Alternative import
    try:
        sys.path.append(os.path.join(current_dir, 'src', 'bot'))
        import whatsapp_bot
        WhatsAppBot = whatsapp_bot.WhatsAppBot
        print("✅ Alternative import berhasil!")
    except ImportError as e2:
        print(f"❌ Alternative import juga gagal: {e2}")
        sys.exit(1)

import time

def test_send_message():
    """Test kirim pesan secara langsung tanpa API"""
    print("🧪 Testing Send Message...")
    
    # Set environment ke non-headless
    os.environ["HEADLESS"] = "false"
    
    try:
        bot = WhatsAppBot()
        
        if not bot.driver:
            print("❌ Tidak dapat membuka WhatsApp Web")
            return
        
        # Login
        if bot.login():
            print("🎉 WhatsApp Web siap digunakan!")
            
            # Test kirim pesan
            phone = input("Masukkan nomor HP (dengan kode negara, contoh: +628123456789): ")
            message = input("Masukkan pesan: ")
            
            print(f"\n🚀 Mengirim pesan '{message}' ke {phone}...")
            result = bot.send_message(phone, message)
            print(f"\n📋 Hasil: {result}")
            
            # Biarkan browser terbuka untuk inspeksi
            input("\n⏸️  Browser akan tetap terbuka. Tekan Enter untuk menutup...")
        else:
            print("❌ Login gagal")
        
    except KeyboardInterrupt:
        print("\n⏹️  Dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Jangan tutup browser otomatis untuk debugging
        try:
            input("Tekan Enter untuk menutup browser...")
            bot.close()
        except:
            pass

if __name__ == "__main__":
    test_send_message()