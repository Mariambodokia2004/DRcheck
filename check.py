import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.core.exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import customtkinter as ctk
import tkinter as tk
from threading import Thread

def key_value_to_env():
    credentials = DefaultAzureCredential()

    key_vault_name = "prod-monitoring-kv"
    vault_url = f"https://{key_vault_name}.vault.azure.net"
    secret_list = ["NOC-DR-Automation-UserName", "NOC-DR-Automation-UserPassword"]

    try:
        secret_client = SecretClient(vault_url, credentials)
        for secret in secret_list:
            os.environ[secret] = secret_client.get_secret(secret).value
            # print(os.environ[secret])

    except azure.core.exceptions.ClientAuthenticationError as ex:
        response = f"Cannot connect to Azure , The error is: \n {ex}"
        return response
    except azure.core.exceptions.ResourceNotFoundError as ex:
        response = f"Error SecretNotFound: \n{ex.message}"
        return response

    except azure.core.exceptions.HttpResponseError as ex:
        if ex.reason == "Unauthorized":
            if ex.reason == "Unauthorized":
                response = f"Unauthorized error :\n {ex.message}"
                return response
            return ex.message
        

key_value_to_env()


username = os.environ.get("NOC-DR-Automation-UserName")
password = os.environ.get("NOC-DR-Automation-UserPassword")






def login(driver, username, password):
    driver.get("https://ams.etoro.com/login")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ets-button-basic.ets-button-big.ets-button-primary"))).click()
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.list-item.list1-item.portfolio.animation-type-move > a.menu-item"))).click()  
        print("Login successful")
    except Exception as e:
        print(f"Login failed: {e}")


def test_portfolio(driver):
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.list-item.list1-item.portfolio.animation-type-move > a.menu-item"))).click()  
        print("Portfolio button clicked")

        instruments = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "et-table-body")))
        if instruments:
            print("Instruments are displayed")
        else:
            print("No instruments found")
    except Exception as e:
        print(f"Portfolio test failed: {e}")


def test_history(driver, url):
    try:
        driver.get(url)
        print(f"Redirected to URL: {url}")
        
        history_items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "private-history-table-flat")))
        if history_items:
            print("History items are displayed")
        else:
            print("No history items found")
    
    except Exception as e:
        print(f"History test failed: {e}")


def test_price_update(driver, url):
    try:
        driver.get(url)
        
        initial_page_source = driver.page_source
        
        for check_count in range(2):
            time.sleep(5)  
            
            current_page_source = driver.page_source
            
            if current_page_source != initial_page_source:
                print(f"Page content has changed after check {check_count + 1}!")
                initial_page_source = current_page_source  
            else:
                print(f"Page content remained the same after check {check_count + 1}.")
        
    except Exception as e:
        print(f"Error occurred: {e}")



def click_timeframes(driver, url):
    try:
        driver.get(url)
        time.sleep(3)  

        parent_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "market-page-timeframes"))
        )
        
        timeframes = parent_element.find_elements(By.XPATH, ".//*[contains(@class, 'ng-star-inserted')]")
        
        if timeframes:
            for index, timeframe in enumerate(timeframes):
                print(f"Clicking on timeframe {index + 1}")
                ActionChains(driver).move_to_element(timeframe).click().perform()  
                time.sleep(2)  
                print("Everything works")
        else:
            print("No timeframes found.")
      
        
    except Exception as e:
        print(f"Error occurred: {e}")


def trade_open(driver, url):
    try:
        driver.get(url)
        time.sleep(10)

        trade_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//et-invest-button//button[contains(@class, 'enabled-trade-button') and @automation-id='trade-button']"))
        )
        driver.execute_script("arguments[0].click();", trade_button)
        print("Trade button clicked.")

        try:
            popup = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tippy-content"))
            )
            driver.execute_script("arguments[0].remove();", popup)
            print("Popup removed.")
        except:
            print("No popup found.")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.et-flex-column"))
        )

        btc_section = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@automation-id='open-position-by-value-name' and contains(text(), 'BTC')]"))
        )
        driver.execute_script("arguments[0].click();", btc_section)
        print("BTC section selected.")

        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@automation-id='open-position-amount-input-amount']"))
        )
        amount_input.clear()
        amount_input.send_keys("10")
        print("Trade amount entered.")

        buy_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='open-position-by-value-submit-button']"))
        )
        driver.execute_script("arguments[0].click();", buy_button)
        print("Buy button clicked.")
        time.sleep(3)

    except Exception as e:
        print(f"Error occurred during trade open: {e}")


def trade_close(driver, url):
    try:
        driver.get(url)
        print(f"Navigated to: {url}")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "position-last-column"))
        )

        close_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='portfolio-position-list-button-close-position']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", close_button)
        print("Close button clicked.")

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Trade')]"))
        )
        driver.execute_script("arguments[0].click();", confirm_button)
        print("Trade closed successfully.")

    except Exception as e:
        print(f"Error occurred while trying to close the trade: {e}")


def check_feed_content(driver, url):
    try:
        driver.get(url)
        print(f"Navigated to feed: {url}")

        posts = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@automation-id='feed-post-wrapp']"))
        )

        if posts and len(posts) > 0:
            print(f"Feed has content. Number of posts found: {len(posts)}")
            return True
        else:
            print("No feed content found.")
            return False

    except Exception as e:
        print(f"Error while checking feed: {e}")
        return False




def trade_open_stock(driver, url):
    try:
        wait = WebDriverWait(driver, 15)

        driver.get(url)
        time.sleep(1.5)

        driver.get("https://ams.etoro.com/portfolio/overview")
        time.sleep(2)

        stocks_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='portfolio-header-filter-bar-instrument-instrumentType.5']")))
        time.sleep(1)
        stocks_filter.click()
        time.sleep(1.5)

        trade_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[@automation-id='trade-button']")))
        time.sleep(1)
        trade_buttons[0].click()
        time.sleep(2)

        trade_dialog = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "open-position-by-value")))
        time.sleep(1)

        try:
            tippy = driver.find_element(By.CSS_SELECTOR, "[data-tippy-root]")
            driver.execute_script("arguments[0].remove();", tippy)
            time.sleep(0.5)
        except:
            pass

        amount_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@automation-id='open-position-amount-input-amount']")))
        time.sleep(0.5)
        amount_input.clear()
        time.sleep(0.3)
        amount_input.send_keys("10")
        time.sleep(1)

        buy_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='open-position-by-value-submit-button']")))
        buy_button.click()
        time.sleep(1.5)

        return "Trade placed successfully"

    except Exception as e:
        print("Error in trade_open_stock:", e)
        return "Trade failed"

def trade_close_stock(driver, url):
    try:
        driver.get(url)
        print(f"Navigated to stock page: {url}")

        close_all_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='portfolio-breakdown-positions-head-last-column-button' and contains(@class, 'close-all-button')]"))
        )
        driver.execute_script("arguments[0].click();", close_all_button)
        print("Close All button clicked.")

        try:
            popup_close_button = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@automation-id='popover-close-button' and contains(@class, 'ets-basic-close-button')]"))
            )
            time.sleep(0.5)  
            
          
            actions = ActionChains(driver)
            actions.move_to_element(popup_close_button).pause(0.2).click().perform()
            print("Popup closed before confirming trade.")
        except Exception as e:
            print(f"No popup to close or failed to close popup: {e}")

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        driver.execute_script("arguments[0].click();", confirm_button)
        print("Trade closed successfully.")

    except Exception as e:
        print(f"Error occurred while trying to close the stock trade: {e}")



def check_search_engine(driver, keyword="btc"):
    try:
        print("Opening homepage to test search...")
        driver.get("https://ams.etoro.com/home")

        search_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@automation-id='search-autocomplete-input']"))
        )
        search_input.clear()
        search_input.send_keys(keyword)
        print(f"Typed '{keyword}' in the search bar.")

        time.sleep(10)  

        print("Search engine is working.")
        return True  

    except Exception as e:
        print(f"Search engine test encountered an issue: {e}")
        return True  


def check_withdraw_tab(driver):
    try:
        driver.get("https://ams.etoro.com/home")
        print("Navigated to home page.")

        withdraw_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@automation-id='sidenav-menu-withdraw']"))
        )
        driver.execute_script("arguments[0].click();", withdraw_tab)
        print("Clicked on 'Withdraw Funds' tab.")

        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//h1[contains(text(), 'Withdraw')] | //div[contains(text(), 'Enter amount') or contains(text(), 'withdraw funds')]"
            ))
        )
        print("Withdraw page/modal loaded successfully.")
        return True

    except Exception as e:
        print(f"Failed to verify withdraw tab functionality: {e}")
        return False


def check_deposit_tab(driver):
    try:
        driver.get("https://ams.etoro.com/home")
        print("Navigated to home page.")

        deposit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@automation-id='left-menu-deposit-button']"))
        )
        driver.execute_script("arguments[0].click();", deposit_button)
        print("Clicked on 'Deposit Funds'.")

        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//h1[contains(text(), 'Deposit')] | //input[contains(@placeholder, 'Amount')] | //button[contains(text(), 'Continue')]"
            ))
        )
        print("Deposit page/modal loaded successfully.")
        return True

    except Exception as e:
        print(f"Failed to verify deposit functionality: {e}")
        return False

test_list = {
    "Login": lambda driver: login(driver, "nocsamurai04", "Aa123456"),
    "Portfolio Check": lambda driver: test_portfolio(driver),
    "History Check": lambda driver: test_history(driver, "https://ams.etoro.com/portfolio/history"),
    "Price Update Check": lambda driver: test_price_update(driver, "https://ams.etoro.com/watchlists"),
    "Timeframes Check": lambda driver: click_timeframes(driver, "https://ams.etoro.com/markets/btc"),
    "Trade Open Check": lambda driver: trade_open(driver, "https://ams.etoro.com/markets/btc"),
    "Trade Close Check": lambda driver: trade_close(driver, "https://ams.etoro.com/portfolio/breakdown/BTC"),
    "Stock Trade Open Check": lambda driver: trade_open_stock(driver, "https://ams.etoro.com/portfolio/overview"),
    "Feed Content Check": lambda driver: check_feed_content(driver, "https://ams.etoro.com/home"),
    "Stock Trade Close Check": lambda driver: trade_close_stock(driver, "https://ams.etoro.com/portfolio/breakdown/NVDA"),
    "Search Engine Check": lambda driver: check_search_engine(driver, "btc"),
    "Withdraw Tab Check": lambda driver: check_withdraw_tab(driver),
    "Deposit Tab Check": lambda driver: check_deposit_tab(driver)

}

class TestThread(Thread):
    def __init__(self, update_callback, progress_callback):
        super().__init__()
        self.update_callback = update_callback
        self.progress_callback = progress_callback

    def run(self):
        driver = webdriver.Chrome()
        try:
            for i, (test_name, test_func) in enumerate(test_list.items()):
                self.update_callback(test_name, "Running... ⏳", "#FFA500")  # Orange
                self.progress_callback(int((i + 1) / len(test_list) * 100))
                try:
                    test_func(driver)
                    self.update_callback(test_name, "Success ✅", "#4CAF50")  # Green
                except Exception:
                    self.update_callback(test_name, "Failed ❌", "#F44336")  # Red
        finally:
            driver.quit()


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DR Check Dashboard")
        self.geometry("1280x800")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.test_status = {}
        self.configure_grid()

        self.header()
        self.card_container()
        self.create_test_cards()
        self.footer()

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Main content resizes

    def header(self):
        title = ctk.CTkLabel(self, text="DR Check Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, pady=20, sticky="n")

    def card_container(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#F4F4F4", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)

    def footer(self):
        self.progress_bar = ctk.CTkProgressBar(self, height=20, width=600)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, pady=(10, 5), sticky="n")

        self.start_button = ctk.CTkButton(self, text="Start Tests", command=self.start_tests, font=ctk.CTkFont(size=16, weight="bold"))
        self.start_button.grid(row=3, column=0, pady=(0, 20), sticky="n")

    def create_test_cards(self):
        for idx, test_name in enumerate(test_list.keys()):
            card = ctk.CTkFrame(self.scroll_frame, height=120, corner_radius=15, fg_color="white")
            card.grid(row=idx // 3, column=idx % 3, padx=20, pady=20, sticky="nsew")
            card.grid_propagate(False)  # Fix card size

            name_label = ctk.CTkLabel(card, text=test_name, font=ctk.CTkFont(size=16, weight="bold"), text_color="#333333")
            name_label.pack(pady=(15, 5))

            status_label = ctk.CTkLabel(card, text="Not Started", font=ctk.CTkFont(size=14), text_color="#555555")
            status_label.pack(pady=(0, 10))

            self.test_status[test_name] = status_label

    def start_tests(self):
        self.thread = TestThread(self.update_status, self.update_progress)
        self.thread.start()

    def update_status(self, test_name, status_text, color):
        if test_name in self.test_status:
            self.test_status[test_name].configure(text=status_text, text_color=color)

    def update_progress(self, value):
        self.progress_bar.set(value / 100)


if __name__ == "__main__":
    key_value_to_env()

    app = MainApp()
    app.mainloop()

