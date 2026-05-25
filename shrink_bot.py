import sys
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

def print_log(text):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}", flush=True)
    sys.stdout.flush()

def manusiawi_scroll(driver):
    """Simulasi membaca halaman: scroll turun-naik secara acak sebelum klik"""
    try:
        total_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(1, random.randint(3, 5)):
            target_scroll = int(total_height * (i / 5))
            driver.execute_script(f"window.scrollTo(0, {target_scroll});")
            time.sleep(random.uniform(1.2, 2.8))
        driver.execute_script(f"window.scrollTo(0, {int(total_height * 0.3)});")
        time.sleep(1)
    except Exception:
        pass

def bypass_shrinkme(target_url):
    print_log(">>> Menyiapkan Undetected WebDriver untuk GitHub Actions...")
    
    options = uc.ChromeOptions()
    # Wajib headless di GitHub Actions karena server tidak memiliki tampilan grafis (GUI)
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")
    
    # Menjalankan chrome dengan library penyamar sidik jari digital
    driver = uc.Chrome(options=options, version_main=124)
    driver.set_window_size(1366, 768) 
    wait = WebDriverWait(driver, 25)
    
    try:
        # 🟢 CEK IP RUNNER GITHUB YANG SEDANG AKTIF
        try:
            driver.get("https://api.ipify.org")
            ip_addr = driver.find_element(By.TAG_NAME, "body").text
            print_log(f"🌍 IP RUNNER GITHUB AKTIF SAAT INI: {ip_addr.strip()}")
            print_log("-" * 50)
        except Exception:
            print_log("⚠️ Gagal mengecek IP Runner, mencoba melanjutkan...")

        print_log(f"🔗 Membuka Target Link: {target_url}")
        driver.get(target_url)
        time.sleep(random.randint(6, 9))
        
        # --- TAHAP 1: Verifikasi & Klik Tombol Continue ---
        manusiawi_scroll(driver)
        print_log("⏳ Mencari tombol Continue / Verifikasi...")
        
        continue_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@id, 'btn')] | //a[contains(text(), 'Click here to continue')] | //button[contains(text(), 'Continue')] | //div[contains(@id, 'link')]//button")
        ))
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
        time.sleep(random.uniform(1.5, 3.5))
        
        actions = ActionChains(driver)
        actions.move_to_element(continue_btn).pause(random.uniform(0.6, 1.4)).click().perform()
        print_log("✅ Tombol pertama berhasil diklik.")
        time.sleep(5)
        
        # --- TAHAP 2: Penanganan Tab Iklan Baru (Pop-Under) ---
        main_window = driver.current_window_handle
        all_windows = driver.window_handles
        
        if len(all_windows) > 1:
            print_log("🌐 Mendeteksi tab iklan terbuka. Mengalihkan fokus agar impresi valid...")
            for window in all_windows:
                if window != main_window:
                    driver.switch_to.window(window)
                    break
            
            waktu_iklan = random.randint(10, 15)
            print_log(f"⏳ Menetap di tab iklan selama {waktu_iklan} detik...")
            time.sleep(waktu_iklan)
            
            driver.close()
            driver.switch_to.window(main_window)
            print_log("✅ Kembali ke halaman utama.")
            
        # --- TAHAP 3: Menunggu Countdown & Ambil Get Link ---
        manusiawi_scroll(driver)
        print_log("⏳ Menunggu countdown timer selesai (15 detik)...")
        time.sleep(16) 
        
        print_log("🔍 Mencari tombol final 'Get Link'...")
        get_link_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Get Link')] | //div[contains(@id, 'go-link')]//a | //button[contains(text(), 'Get Link')]")
        ))
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", get_link_btn)
        time.sleep(random.uniform(1.0, 2.5))
        
        try:
            actions.move_to_element(get_link_btn).pause(random.uniform(0.4, 1.0)).click().perform()
        except Exception:
            driver.execute_script("arguments[0].click();", get_link_btn)
            
        print_log("🎉 Sukses memicu konversi Get Link!")
        time.sleep(6)

    except Exception as e:
        print_log(f"❌ Terjadi kendala atau mendeteksi Captcha keras: {str(e)}")
        
    finally:
        driver.quit()
        print_log("🏁 Sesi browser ditutup.\n" + "-"*50)

if __name__ == "__main__":
    print_log("🚀 MEMULAI BOT OTOMASI SHRINKME DI GITHUB ACTIONS...")
    
    # Target link spesifik milikmu
    target_link = "https://shrinkme.click/Blogheru"
    
    # Jalankan bot
    bypass_shrinkme(target_link)

