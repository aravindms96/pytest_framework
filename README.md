# pytest_framework

This project is designed to automate the testing of a web application using Python and the pytest framework. It follows the Page Object Model (POM) design pattern to promote scalability, reusability, and ease of maintenance.

## **📁 Project Structure**

![image](https://github.com/user-attachments/assets/d0dbb42a-691b-4845-9d87-f3b4e5dbafa9)

## **🔧 Key Components Explained**
**conftest.py**: Defines shared fixtures and hooks to manage test setup and teardown processes, enhancing modularity and reducing code duplication.

**settings.toml**: Houses configurable parameters such as environment URLs, credentials, and other settings, facilitating easy adjustments across different test environments.

**pages/**: Contains Page Object Model classes that abstract UI elements and user interactions, promoting code reusability and readability.

**utils/**: Encompasses utility modules providing services like configuration management, data handling, browser driver management, logging, and session caching.

**tests/**: Hosts test modules written using pytest, each containing test functions that validate specific functionalities of the web application.

**Reports/**: Stores HTML reports generated after test executions, offering a comprehensive overview of test results.

**PytestLogs/**: Maintains log files that record detailed information about test runs, aiding in debugging and analysis.


# **✅ Prerequisites**
1. Before initiating the test execution, ensure the following are set up on your system:
 1. **Python Installation**: Python version 3.11 or higher should be installed. Confirm the installation by running python --version in your command prompt or terminal.
 2. **Environment Variables**: The Python installation path should be added to your system's environment variables to allow seamless execution from the command line.
 3. **Google Chrome Browser**: Install Google Chrome browser versions 136.0.7103.92 or 136.0.7103.93 (64-bit) to ensure compatibility with the ChromeDriver used in the framework.

# **🚀 Steps to Execute Test Cases**

Extract the Project:

  1. Download and extract the project archive to a preferred directory on your system.
  2. Navigate to Project Directory:
     * Open the command prompt or terminal.
      * Change the directory to the extracted project folder:
        ```cmd
        cd path\to\your\project\framework
        ```
  3. Execute the Test Suite:
     * Run the provided batch file to initiate the test execution:
       ```cmd
       test_executor.bat
       ```
  4. This script performs the following actions:
     * Installs all necessary Python packages listed in requirements.txt.
      * Triggers the execution of all test cases using pytest.
  5. Monitor Test Execution:
     * Upon completion, a summary indicating the number of passed and failed test cases will be presented.
  6. Post-Execution Artifacts:
     * HTML Test Report:
      1. An HTML report detailing the test execution results is generated and stored in the Reports directory:
     ```directory
     Your_Project_Directory\Reports\TestReport_<timestamp>.html
     ```
      * Execution Logs:
       1. Comprehensive logs capturing the execution details are saved in the PytestLogs directory:
      ```directory
      Your_Project_Directory\PytestLogs\app.log
      ```


**📝 Additional Notes**

* Browser Compatibility: Ensure that the Chrome browser version installed matches the version compatible with the chromedriver.exe provided in the utils\chromedriver-win64 directory. Mismatched versions may lead to execution failures.

* Virtual Environments: For better dependency management and to avoid conflicts with other Python projects, consider using a virtual environment. You can set one up using venv or virtualenv before installing the required packages.

* Test Customization: The settings.toml file contains environment-specific configurations. Modify this file to suit different testing environments or scenarios.

* Extending Tests: To add new test cases, create additional Python files in the tests directory following the naming convention test_*.py. Utilize pytest fixtures and the Page Object Model classes defined in the pages directory to structure your tests effectively.



**✅ Best Practices Incorporated**
* Modular Design: Adopts the Page Object Model to separate test logic from page structure, enhancing maintainability.

* Configuration Management: Utilizes a centralized configuration file (settings.toml) to manage environment-specific settings efficiently.

* Logging and Reporting: Implements structured logging and generates detailed HTML reports to facilitate test result analysis.

* Dependency Management: Lists all required Python packages in requirements.txt to ensure consistent environment setup.
