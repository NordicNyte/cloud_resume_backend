import logging  # For logging events and debugging
import pytest  # For writing and running tests
from playwright.sync_api import sync_playwright  # For browser automation and web testing
import time  # For the retry loop

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s - %(message)s', force=True)
logger = logging.getLogger(__name__)

# Define the Cloud Resume URL 
RESUME_URL = 'https://aidantaggart.com'
# Define the first name to verify in the resume heading
FNAME = 'Aidan'

def test_cloud_resume_e2e():
    """
    End-to-end test for the Cloud Resume website.

    This test performs the following actions:
    1. Opens a browser and navigates to the Cloud Resume website using Playwright.
    2. Verifies that the resume content is displayed on the page by checking the visibility 
       of the H1 heading and asserting the presence of a specific text (FNAME).
    3. Captures the initial visitor count from an element with the ID 'visitor-counter'.
    4. Refreshes the page to simulate a new visit to the website.
    5. Captures the updated visitor count after the page reload and verifies that the visitor count 
       has incremented by 1.
    6. If the visitor count increments correctly, the test passes.
    7. Closes the browser.

    Assertions:
    - The resume heading (H1) is visible and contains the expected name (FNAME).
    - The visitor count is a valid integer and increments by 1 after the page is refreshed.
    - If any of these conditions fail, the test will log an error message and fail.

    Raises:
    - ValueError: If the visitor count cannot be converted to an integer.
    - AssertionError: If the resume heading is not visible or the visitor count does not increment as expected.

    To run this test, use pytest:
    - pytest -vs
    - pytest -vs test_cloud_resume_e2e.py
    """

    # Start Playwright and open a browser
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)  # Launches the browser, set headless=True for no UI
        page = browser.new_page()

        # Navigate to the Cloud Resume website
        logger.info(f"Navigating to {RESUME_URL}")
        page.goto(RESUME_URL)

        # Verify the resume content is displayed
        resume_heading = page.locator('h1')
        assert resume_heading.is_visible(), "Error: Resume heading is not visible"
        
        resume_text = resume_heading.inner_text()
        logger.info(f"Resume heading text: {resume_text}")
        assert FNAME in resume_text, f"Error: '{FNAME}' text not found in resume heading"

        # Capture the initial visitor count with a retry loop
        logger.info("Capturing the initial visitor count")
        page.wait_for_selector('#visitor-counter', timeout=5000)  # Wait for the visitor counter element
        visitor_counter = page.locator('#visitor-counter')
        
        retries = 5  # Number of attempts to retrieve a valid count
        initial_count_text = ""
        for attempt in range(retries):
            initial_count_text = visitor_counter.inner_text().strip()
            if initial_count_text.isdigit():
                break
            logger.info(f"Attempt {attempt + 1}: Visitor counter not loaded yet, retrying...")
            time.sleep(1)  # Wait 1 second before retrying
        
        assert initial_count_text.isdigit(), f"Visitor count is missing or not a valid integer. Response body: '{initial_count_text}'"
        initial_count = int(initial_count_text)
        logger.info(f"Initial visitor count retrieved: {initial_count}")

        # Refresh the page to simulate a new visit
        logger.info("Refreshing the page to simulate a new visit")
        page.reload()

        # Verify the visitor count has incremented by 1
        logger.info("Capturing the updated visitor count after page reload")
        page.wait_for_selector('#visitor-counter', timeout=5000)  
        
        # Retry to capture updated visitor count
        updated_count_text = ""
        for attempt in range(retries):
            updated_count_text = visitor_counter.inner_text().strip()
            if updated_count_text.isdigit():
                break
            logger.info(f"Attempt {attempt + 1}: Updated visitor counter not loaded yet, retrying...")
            time.sleep(1)  # Wait 1 second before retrying
        
        assert updated_count_text.isdigit(), f"Updated visitor count is missing or not a valid integer. Response body: '{updated_count_text}'"
        updated_count = int(updated_count_text)
        logger.info(f"Updated visitor count retrieved: {updated_count}")

        # Assert the visitor count incremented by 1
        assert updated_count == initial_count + 1, f"Error: Expected visitor count to increment by 1, but got {updated_count}"
        logger.info(f"Test passed: Visitor count incremented from {initial_count} to {updated_count}")

        # Close the browser
        logger.info("Closing the browser")
        browser.close()