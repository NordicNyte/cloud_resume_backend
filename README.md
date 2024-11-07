# Cloud Resume Challenge - Backend

This repository contains the backend components for the Cloud Resume Challenge, designed to handle and test visitor counts for a static resume website hosted on AWS. The backend is built to interact with a DynamoDB table that tracks visitor counts, and it includes tests for functionality verification.

## Repository Structure

- **`lambda_function.py`**: Main Lambda function script responsible for handling API requests to retrieve and update the visitor count in DynamoDB.
- **`tests/`**: Directory containing test scripts for the backend functionality.
  - **`test_cloud_resume_e2e.py`**: End-to-end test that simulates a visit to the Cloud Resume website and verifies visitor count functionality using Playwright.
  - **`test_lambda_unit.py`**: Unit tests for the Lambda function.
  - **`test_visitor_counter_system.py`**: System test for validating the visitor counter API.
- **`venv/`**: Virtual environment directory (should be excluded from version control) containing dependencies required to run the backend and tests.
- **`requirements.txt`**: Lists all Python packages needed to run the backend, including `boto3` for AWS interactions, `requests` for HTTP requests, and `pytest` for testing.
- **`pytest.ini`**: Configuration file for pytest, specifying any custom settings for running tests.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd backend
2. **Set Up Virtual Environment**:
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

3. **Install Dependencies**:
   - Install all necessary Python packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run Tests**:
   - Use `pytest` to run the test suite and validate functionality:
     ```bash
     pytest -vs
     ```

## Deployment Instructions

1. **Package the Lambda Function**:
   - Zip the `lambda_function.py` file and any necessary dependencies:
     ```bash
     zip -r lambda_function.zip lambda_function.py
     ```

2. **Deploy to AWS Lambda**:
   - Upload the `lambda_function.zip` file to your AWS Lambda function through the AWS Management Console.
   - Configure the Lambda function to connect to your DynamoDB table (e.g., `visitor_count`).
   - Set environment variables if needed (e.g., DynamoDB table name, region).

3. **Configure API Gateway**:
   - Create a new API in API Gateway and connect it to your Lambda function.
   - Set up an endpoint that allows the necessary HTTP methods (e.g., `GET`, `POST`).
   - Enable CORS if your frontend is hosted on a different domain.

4. **Verify the Deployment**:
   - Test the API Gateway endpoint by making a request to ensure it connects to the Lambda function.
   - Confirm the visitor count in DynamoDB updates as expected when the endpoint is accessed.
