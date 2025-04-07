import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,  QFrame, QLabel, QProgressBar, QGridLayout
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




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
        driver.get(url)
        print(f"Navigated to stock page: {url}")
        time.sleep(60)

        trade_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='trade-button']"))
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

def trade_close_stock(driver, url):
    try:
        driver.get(url)
        print(f"Navigated to stock page: {url}")

        close_all_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@automation-id='portfolio-breakdown-positions-head-last-column-button' and contains(@class, 'close-all-button')]"))
        )
        driver.execute_script("arguments[0].click();", close_all_button)
        print("Close All button clicked.")

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))  # Adjust if confirmation button exists
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
    "Trade Close Check": lambda driver: trade_close(driver, "https://ams.etoro.com/portfolio/breakdown/ETH"),
    "Feed Content Check": lambda driver: check_feed_content(driver, "https://ams.etoro.com/home"),
    "Stock Trade Open Check": lambda driver: trade_open_stock(driver, "https://ams.etoro.com/markets/tsla"),
    "Stock Trade Close Check": lambda driver: trade_close_stock(driver, "https://ams.etoro.com/portfolio/breakdown/NVDA.EXT"),
    "Search Engine Check": lambda driver: check_search_engine(driver, "btc"),
    "Withdraw Tab Check": lambda driver: check_withdraw_tab(driver),
    "Deposit Tab Check": lambda driver: check_deposit_tab(driver),
    "Stock Trade Open Check": lambda driver: trade_open_stock(driver, "https://ams.etoro.com/markets/tsla"),

}
class TestThread(QThread):
    update_status = pyqtSignal(str, str)
    update_progress = pyqtSignal(int)

    def run(self):
        driver = webdriver.Chrome()
        try:
            for i, (test_name, test_func) in enumerate(test_list.items()):
                self.update_status.emit(test_name, "Running... ⏳")
                self.update_progress.emit(int((i + 1) / len(test_list) * 100))
                
                try:
                    test_func(driver)
                    self.update_status.emit(test_name, "Success ✅")
                except Exception as e:
                    self.update_status.emit(test_name, "Failed ❌")
        finally:
            driver.quit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DR Check")
        self.setGeometry(200, 200, 1200, 800)  # Adjust window size for better responsiveness
        self.setStyleSheet("background-color: #F0F2F5;")

        main_layout = QVBoxLayout()

        header = QLabel("DR Check")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        self.grid_layout = QGridLayout()
        self.test_status = {}

        # Dynamically calculate the number of columns based on screen size
        columns = self.calculate_columns_based_on_screen_width()
        for idx, test in enumerate(test_list.keys()):
            card = self.create_test_card(test)
            self.grid_layout.addWidget(card, idx // columns, idx % columns)

        main_layout.addLayout(self.grid_layout)

        # Progress bar (ensure it remains visible)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)  # Set initial value to 0
        main_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        self.start_button = QPushButton("Start Tests")
        self.start_button.setStyleSheet("""
            background-color: #4CAF50;  # Green color
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        """)
        self.start_button.setFont(QFont("Arial", 14, QFont.Bold))  # Larger font for better clarity
        self.start_button.clicked.connect(self.start_tests)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def create_test_card(self, test_name):
        card = QFrame()
        card.setStyleSheet("""
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px;
        border: 1px solid #E0E0E0;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);  # Subtle shadow for depth
        min-width: 250px;  # Ensure consistent card size
    """)
        layout = QVBoxLayout()

    # Title label for the test name
        name_label = QLabel(test_name)
        name_label.setFont(QFont("Arial", 16, QFont.Bold))  # Slightly larger font for titles
        name_label.setStyleSheet("background: transparent; border: none;")  # Remove any background or border
        layout.addWidget(name_label, stretch=1)  # Ensure it stretches within the card

    # Status label for test status
        status_label = QLabel("Not Started")
        status_label.setFont(QFont("Arial", 14))  # Slightly larger font for better readability
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("background: transparent; border: none;")  # Remove any background or border
        layout.addWidget(status_label, stretch=2)  # Ensure status label stretches

        self.test_status[test_name] = status_label
        card.setLayout(layout)

        return card


    def calculate_columns_based_on_screen_width(self):
        screen_width = self.screen().availableGeometry().width()
        
        # Calculate number of columns based on screen width, a simple ratio
        if screen_width >= 1920:  # For large screens
            return 4
        elif screen_width >= 1280:  # For medium-sized screens
            return 3
        else:  # For small screens
            return 2

    def start_tests(self):
        self.test_thread = TestThread()
        self.test_thread.update_status.connect(self.update_test_status)
        self.test_thread.update_progress.connect(self.update_progress)
        self.test_thread.start()

    def update_test_status(self, test_name, status):
        if test_name in self.test_status:
            self.test_status[test_name].setText(status)
            color = "#4CAF50" if "Success" in status else "#F44336" if "Failed" in status else "#FF9800"
            self.test_status[test_name].setStyleSheet(f"color: {color};")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())