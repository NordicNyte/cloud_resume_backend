import requests
import pytest

# Define the API endpoint URL
API_URL = 'https://q123oxa8h3.execute-api.us-east-1.amazonaws.com/dev/visitorCounter'

def test_visitor_counter_system():
    """
    Test the visitor counter API to ensure it increments the visitor count correctly.
    """

    # Make the first request to get the initial visitor count
    print("\nMaking the first request to get the initial visitor count")
    response = requests.get(API_URL)
    
    # Check the response status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Check if the response contains a valid visitor count in JSON format
    print(f"Checking if the response contains a valid visitor count")
    try:
        data = response.json()  # Parse JSON response
        initial_count = data.get("visitor_count")
        assert isinstance(initial_count, int), f"Expected visitor count to be an integer, got {type(initial_count)}"
        print(f"Initial visitor count retrieved: {initial_count}")
    except (ValueError, KeyError, TypeError) as e:
        pytest.fail(f"Visitor count is missing or not in expected format. Response body: '{response.text}'")

    # Make the second request to increment the visitor count
    print("Making the second request to increment the visitor count")
    response = requests.get(API_URL)
    
    # Check the status code again
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Ensure the visitor count has incremented by 1
    updated_data = response.json()
    updated_count = updated_data.get("visitor_count")
    assert isinstance(updated_count, int), f"Expected updated visitor count to be an integer, got {type(updated_count)}"
    assert updated_count == initial_count + 1, f"Expected visitor count to increment by 1, but got {updated_count} instead of {initial_count + 1}"
    
    # Print success message for debugging purposes
    print(f"Test passed: Visitor count incremented from {initial_count} to {updated_count}")
