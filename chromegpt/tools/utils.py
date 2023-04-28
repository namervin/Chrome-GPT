"""Utils for chromegpt tools."""

import re
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

### Main Content Extraction ###
def is_complete_sentence(text: str) -> bool:
    return re.search(r'[.!?]\s*$', text) is not None

def get_all_text_elements(driver: WebDriver) -> List[str]:
    xpath = "//*[not(self::script or self::style or self::noscript)][string-length(normalize-space(text())) > 0]"
    elements = driver.find_elements(By.XPATH, xpath)
    texts = [element.text.strip() for element in elements if element.text.strip() and element.is_displayed() and element_completely_viewable(driver, element)]
    return texts

def find_interactable_elements(driver: WebDriver) -> List[str]:
    # Extract interactable components (buttons and links)
    buttons = driver.find_elements(By.XPATH, "//button")
    links = driver.find_elements(By.XPATH, "//a")

    interactable_elements = buttons + links

    interactable_output = []
    for element in interactable_elements:
        if element.is_displayed() and element_completely_viewable(driver, element) and element.is_enabled():
            element_text = element.text.strip()
            if element_text and element_text not in interactable_output:
                element_text = prettify_text(element_text, 50)
                interactable_output.append(element_text)
    return interactable_output

def prettify_text(text: str, limit: Optional[int] = None) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = text.strip().lower()
    if limit:
        text = text[:limit]
    return text

def element_completely_viewable(driver, elem):
    elem_left_bound = elem.location.get('x')
    elem_top_bound = elem.location.get('y')
    elem_right_bound = elem_left_bound
    elem_lower_bound = elem_top_bound

    win_upper_bound = driver.execute_script('return window.pageYOffset')
    win_left_bound = driver.execute_script('return window.pageXOffset')
    win_width = driver.execute_script('return document.documentElement.clientWidth')
    win_height = driver.execute_script('return document.documentElement.clientHeight')
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height

    return all((win_left_bound <= elem_left_bound,
                win_right_bound >= elem_right_bound,
                win_upper_bound <= elem_top_bound,
                win_lower_bound >= elem_lower_bound)
              )

def truncate_string_from_last_occurrence(string, character):
    last_occurrence_index = string.rfind(character)
    if last_occurrence_index != -1:
        truncated_string = string[:last_occurrence_index + 1]
        return truncated_string
    else:
        return string