import subprocess
import os
import time
#$ python -m pip install pypdf2

#import PyPDF2

page_n = 1003
url = f"https://www.mcmaster.com/catalog/128/{page_n}/"
fname = f"page-{page_n}.pdf"


good_url = "https://www.mcmaster.com/4464K12/"
bad_url = "https://www.mcmaster.com/4464X12/"


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def perform_actions(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(2)
    print('Performing Actions!')
    actions.perform()

driver = webdriver.Chrome()
driver.delete_all_cookies()

driver.execute_script("window.open('')")  # Create a separate tab than the main one
driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 + Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
driver.close()  # Close that window
driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.


driver.get(good_url)

# Wait for the page to load
driver.implicitly_wait(30)

# Get the rendered HTML of the page
html = driver.page_source

# Save the HTML to a file
with open('good.html', 'w') as file:
    file.write(html)

time.sleep(30)    
driver.quit()


exit()
if os.path.exists(fname):
    urls = get_pdf_links(fname)
    print(urls)
else:
    print(f'File {fname} does not exist')
