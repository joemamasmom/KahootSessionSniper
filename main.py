import time
import random
import threading
from ascii import logo, sniped
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class COLORS:
    YELLOW = "\033[38;2;255;202;0m"
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WHITE = "\033[00m"

def joinGame(gamePin, nickname, semaphore):
    try:
        print(f"Bot {COLORS.GREEN}{nickname}{COLORS.WHITE} Is Attempting to Connect To {COLORS.GREEN}{gamePin}{COLORS.WHITE}")
        driver = webdriver.Chrome()  # Replace with the appropriate webdriver for your browser

        driver.get("https://kahoot.it")

        wait = WebDriverWait(driver, 10)

        pinInput = wait.until(EC.visibility_of_element_located((By.ID, "game-input")))
        pinInput.send_keys(gamePin)
        pinSubmit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "enter-pin-form__SubmitButton-sc-z047z0-2")))
        pinSubmit.click()

        print(f"Bot {COLORS.GREEN}{nickname}{COLORS.WHITE} Successfully {COLORS.YELLOW}Entered The Pin{COLORS.WHITE}")

        nicknameInput = wait.until(EC.visibility_of_element_located((By.ID, "nickname")))
        nicknameInput.send_keys(nickname)

        joinButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "nickname-form__SubmitButton-sc-1mjq176-1")))
        joinButton.click()

        print(f"Bot {COLORS.GREEN}{nickname}{COLORS.WHITE} Successfully {COLORS.BLUE}Joined The Lobby{COLORS.WHITE}")

        time.sleep(1)
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        semaphore.release()

if __name__ == "__main__":
    usernamesFile = "usernames.txt"
    print(logo)
    gamePin = int(input("Enter the game PIN: "))
    numUsers = int(input("Enter the number of users: "))
    maxConcurrentWindows = int(input("Enter the number of max windows running(7 Max): "))
    
    #using more windows significantly slows the process down depending on your machine
    if maxConcurrentWindows > 7:
        exit
    
    sniped()
    
    with open(usernamesFile, "r") as file:
        nicknames = [line.strip() for line in file]

    randomNicknames = random.sample(nicknames, numUsers)

    semaphore = threading.BoundedSemaphore(maxConcurrentWindows)

    with ThreadPoolExecutor(max_workers=numUsers) as executor:
        for nickname in randomNicknames:
            semaphore.acquire()
            executor.submit(joinGame, gamePin, nickname, semaphore)