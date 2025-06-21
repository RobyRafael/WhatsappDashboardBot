#!/usr/bin/env python3
"""
Script untuk login WhatsApp Web dan scan QR code
Jalankan script ini untuk melakukan initial login
"""

import sys
import os
sys.path.append('src')

from src.bot.whatsapp_bot import WhatsAppBot

def main():
    print("=== WhatsApp Web Login ===")
    print("1. Browser akan terbuka")
    print("2. Scan QR code dengan aplikasi WhatsApp di HP")
    print("3. Tunggu hingga login berhasil")
    print("4. Tekan Ctrl+C untuk keluar\n")
    
    try:
        # Buat bot instance untuk login
        bot = WhatsAppBot(user_data_suffix="login")
        
        # Lakukan login
        if bot.login():
            print("✅ Login berhasil!")
            print("Anda sekarang bisa menggunakan API untuk kirim pesan")
            input("Tekan Enter untuk keluar...")
        else:
            print("❌ Login gagal!")
            
    except KeyboardInterrupt:
        print("\n⚠️ Login dibatalkan")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'bot' in locals():
            bot.close()

if __name__ == "__main__":
    main()