def log_playback(log_file, log_time, mode, i):
    with open(log_file, "a") as file:
        if(mode==0):
            file.write(f"{i} Start: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        else:
            file.write(f"{i} End: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            if(i==19):
                file.write("\n\n")
                
def start_tcpdump(i, j, timestamp,dir_name):
    
    file_path = f"/home/cs1210560/Downloads/{dir_name}/{i}-{j}-{timestamp}.pcapng"

    print(f"Starting tcpdump, saving to {file_path}...")
    duration = 35
    tcpdump_process = subprocess.Popen(
        ["sudo","tcpdump", "-i", "wlxc01c3038dc4b", "-w", file_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    

    print("exiting start")
    return tcpdump_process
    
def stop_tcpdump(tcpdump_process):
    """Stop tcpdump by terminating the process."""
    print("Stopping tcpdump...")
#    os.kill(tcpdump_process.pid)
    subprocess.run(["sudo", "pkill", "tcpdump"])

def play_youtube(youtube_url,i,j):
        driver.switch_to.new_window("tab")
        driver.get(youtube_url)

        video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
        )

        try:
            play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Play']"))
            )
            play_button.click()
        except Exception as e:
            print(f"Error clicking YouTube play button: {e}")

        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return arguments[0].paused;", video) == False
            )
            start_time = datetime.now()
            tcpproc = start_tcpdump(j,i,start_time,"youtube_capture")
            log_playback("youtube_log.txt", start_time, 0,i)
            print(f"YouTube video started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error ensuring YouTube video is playing: {e}")
            return  

        time.sleep(35)
        stop_tcpdump(tcpproc)
        end_time = datetime.now()
        print(f"YouTube video ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_playback("youtube_log.txt", end_time,1,i)
        driver.close()  

        driver.switch_to.window(driver.window_handles[0])


def human_like_mouse_move(start, end, duration=1.0, steps=100):

    def get_curve_points(start, end, num_points=steps):
        control1 = (start[0] + np.random.randint(-100, 100), start[1] + np.random.randint(-100, 100))
        control2 = (end[0] + np.random.randint(-100, 100), end[1] + np.random.randint(-100, 100))
        
        t_values = np.linspace(0, 1, num_points)
        curve_points = []

        for t in t_values:
            x = (1 - t)**3 * start[0] + 3 * (1 - t)**2 * t * control1[0] + 3 * (1 - t) * t**2 * control2[0] + t**3 * end[0]
            y = (1 - t)**3 * start[1] + 3 * (1 - t)**2 * t * control1[1] + 3 * (1 - t) * t**2 * control2[1] + t**3 * end[1]
            curve_points.append((x, y))
        
        return curve_points

    points = get_curve_points(start, end)
    interval = duration / steps

    for point in points:
        pyautogui.moveTo(point[0], point[1], duration=interval)

        time.sleep(abs(np.random.normal(0.005, 0.002)))


def simulate_mouse_movement():
        action = ActionChains(driver)
        for _ in range(10):  
            x_offset = random.randint(0, 20)
            y_offset = random.randint(0, 20)
            action.move_by_offset(x_offset, y_offset).perform()
            time.sleep(0.2)  
def play_hotstar(hotsar_url,i,j):
        driver.switch_to.new_window("tab")
        driver.get(hotstar_url)

        video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
        )

        human_like_mouse_move((100, 200), (300, 400), duration=1.0)
        
        try:
            play_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Play']")))
            play_button.click()
        except Exception as e:
            print(f"Error clicking Hotstar play button: {e}")

        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return arguments[0].paused;", video) == False
            )
            start_time = datetime.now()
            tcpproc = start_tcpdump(j,i,start_time,"hotstar_capture")
            log_playback("hotstar_log.txt", start_time, 0,i)
            print(f"Hotstar video started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error ensuring Hotstar video is playing: {e}")
            return  

        time.sleep(35)
        stop_tcpdump(tcpproc)
        end_time = datetime.now()
        print(f"Hotstar video ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_playback("hotstar_log.txt", end_time,1,i)
        driver.close()  

        driver.switch_to.window(driver.window_handles[0])

# finally:
#     driver.quit()

import time
import subprocess
import os
import random
import numpy as np
import pyautogui
from datetime import datetime,timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument(r"user-data-dir=/home/cs1210560/.config/google-chrome/")
chrome_options.add_argument("profile-directory=Default")  


service = Service(r"/home/cs1210560/Downloads/chromedriver-linux64/chromedriver")  
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(60)


def read_urls(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

youtube_urls = read_urls("youtube_links.txt")
hotstar_urls = read_urls("hotstar_links.txt")
netflix_urls = read_urls("netflix_links.txt")

def play_video(url,i,j):

    driver.switch_to.new_window("tab")
    driver.get(url)

    try:
        
        play_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Play']"))
        )
        play_button.click()
        print("hello")
#         driver.execute_script("document.querySelector('video').currentTime = 45;")

#         driver.execute_script("document.querySelector('video').play();")


        ad_playing = True
        while ad_playing:
            try:
                ad_element = driver.find_element(By.CSS_SELECTOR, ".ad-showing")
                print("Ad detected, waiting for ad to finish...")
                time.sleep(1)  
            except:
                ad_playing = False

        video_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
        )
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return arguments[0].paused;", video_element) == False
        )
        
        start_time = datetime.now()
        tcpproc = start_tcpdump(j,i,start_time,"netflix_capture")
        log_playback("netflix_log.txt", start_time, 0,i)
        print(f"Video started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        time.sleep(35)
        stop_tcpdump(tcpproc)
        end_time = datetime.now()
        print(f"Video ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_playback("netflix_log.txt", end_time,1,i)
    except Exception as e:
        print(f"Error playing video: {e}")
    
    finally:

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

try:
    for i in range(25):
        j = 0
        for youtube_url in youtube_urls:
            play_youtube(youtube_url,j,i)
            j+=1
    for i in range(25):
        j = 0
        for netflix_url in netflix_urls:
            play_video(netflix_url,j,i)
            j+=1
    for i in range(25):
        j = 0
        for hotstar_url in hotstar_urls:
            play_hotstar(hotstar_url,j,i)
            j+=1
        
finally:
    driver.quit()


