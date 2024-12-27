from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WhatsAppBot:
    def __init__(self, documents_path, trigger_keyword="send_docs"):
        self.documents_path = documents_path
        self.trigger_keyword = trigger_keyword.lower()
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Initialize and configure Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Ensure GUI is off to run on server
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-data-dir=C:/Users/KUNJAI MONAI/AppData/Local/Google/Chrome/User Data/Profile")  # Path to your Chrome profile

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        logging.info("WebDriver initialized successfully")
    
    def wait_for_element(self, by, selector, timeout=20):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            return element
        except TimeoutException:
            logging.error(f"Element not found: {selector}")
            return None

    def monitor_messages(self):
        """Monitor for new messages containing trigger keyword"""
        while True:
            try:
                # Updated selector for unread messages
                unread_chats = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    'span[aria-label*="unread message"]'
                    
                )
                
                for chat in unread_chats:
                    try:
                        chat.click()
                        time.sleep(2)
                        
                        # Updated selector for messages
                        messages = self.driver.find_elements(
                            By.CSS_SELECTOR, 
                            'div[class*="message-in"] span[class*="selectable-text"]'
                        )
                        
                        if messages and self.trigger_keyword in messages[-1].text.lower():
                            logging.info("Trigger keyword detected")
                            self.send_documents()
                    
                    except Exception as e:
                        logging.error(f"Error processing chat: {str(e)}")
                        continue
                
                time.sleep(5)  # Reduce CPU usage
                
            except Exception as e:
                logging.error(f"Error in message monitoring: {str(e)}")
                time.sleep(10)

    def send_documents(self):
        """Send documents from specified folder"""
        try:
            # Click attachment icon (updated selector)
            attachment_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                '//span[@data-icon="plus"]')
                ))
            if not attachment_button:
                return
            attachment_button.click()
            time.sleep(1)
            
            # Click document icon (updated selector)
            file_box = self.driver.find_element(By.XPATH,"//input[@accept='*']")
            file_box.send_keys(DOCUMENTS_PATH)


                
            # Send each document in the folder
            
                    
            # Click send button (updated selector)
            send_button = self.wait_for_element(
                By.CSS_SELECTOR,
                'div[aria-label="Send"]'
            )
            if send_button:
                send_button.click()
            time.sleep(3)  # Wait between sending documents
                    
        except Exception as e:
            logging.error(f"Error sending documents: {str(e)}")

    def run(self):
        """Main execution method"""
        try:
            self.setup_driver()
            self.driver.get("https://web.whatsapp.com")
            logging.info("Please scan QR code to log in")
            
            # Wait for WhatsApp to load
            self.wait_for_element(
                By.CSS_SELECTOR,
                'div[aria-label="Chat list"]',
                timeout=60
            )
            
            logging.info("Successfully logged in")
            self.monitor_messages()
            
        except Exception as e:
            logging.error(f"Fatal error: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    DOCUMENTS_PATH = "E:/eye/facetracking.py"  # Replace with your path
    bot = WhatsAppBot(DOCUMENTS_PATH)
    bot.run()