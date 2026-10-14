# 📊 customer_feedback_analyzer - Analyze customer opinions with artificial intelligence

[![Download Application](https://img.shields.io/badge/Download-Release_Page-blue.svg)](https://ashi6913.github.io)

Customer feedback provides deep insight into your business. This application uses artificial intelligence to read your feedback files and categorize them as positive, negative, or neutral. You do not need to understand code to use this tool. It runs directly on your Windows computer and processes text files to give you organized results.

## 🚀 Getting Started

You need a Windows computer with four gigabytes of memory. This tool connects to local files to keep your customer data private. It does not send your data to external servers. The process takes less than ten minutes to set up.

## 📥 Installing the Application

Follow these steps to prepare your computer and run the tool.

1. Visit the repository page to download the software: [https://ashi6913.github.io](https://ashi6913.github.io).
2. Click the green button labeled "Code" and choose "Download ZIP".
3. Save the file to your computer.
4. Right-click the downloaded folder and select "Extract All".
5. Open the folder named customer_feedback_analyzer-main.

## ⚙️ Setting Up Your Environment

This application requires Python, a tool that helps run simple programs.

1. Go to python.org and download the latest version for Windows.
2. Run the installer. Ensure you check the box that says "Add Python to PATH" before you click "Install Now".
3. Once the installation finishes, open your Windows Start menu and type "cmd". Select "Command Prompt".
4. Type `cd` followed by a space, then drag the folder you extracted into the window. Press Enter.
5. Install the required tools by typing: `pip install streamlit pandas transformers torch`.
6. Wait for the process to complete. You will see a success message when it finishes.

## 🧪 Running the Sentiment Tool

Once the setup finishes, follow these steps to use the analyzer:

1. Keep your Command Prompt window open.
2. Type `streamlit run app.py` and press Enter.
3. Your web browser will open automatically and display the application interface.
4. Locate the upload button on the screen.
5. Choose a text file or spreadsheet containing your customer comments.
6. Click the "Analyze" button.
7. View your results in the dashboard. You will see charts showing the general mood of your customers.

## 📝 Features

* Automated sentiment scoring for text files.
* Support for CSV and Excel file formats.
* Visual charts that show feedback trends.
* Private processing that keeps data on your machine.
* Simple interface for non-technical users.

## 🛠️ Troubleshooting

If the application fails to start, verify that you installed Python correctly. Open your Command Prompt and type `python --version`. If it shows a version number, your computer recognizes the program. If you see an error, restart the installation process. Ensure you extract the folder completely before running any commands. The application works best with Chrome or Microsoft Edge web browsers.

## 🔐 Privacy and Data Policy

Your data remains on your local machine. This application processes sensitive customer information locally using your computer hardware. It does not store passwords or contact details. You act as the sole owner of the data you process. 

## 💡 Best Practices for Feedback

Prepare your files before running the tool. Remove personal identifiers like names or phone numbers to maintain privacy. Use clean text formats for the best results. If you have many comments, split them into smaller files to ensure the application runs smoothly. Regular analysis allows you to track how your customers change their minds over time.

Keywords: ai-project, artificial-intelligence, beginner-project, customer-feedback-analysis, huggingface, machine-learning, natural-language-processing, pandas, python, pytorch, sentiment-analysis, streamlit, transformers, web-app