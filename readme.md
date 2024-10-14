# Summarizer Agent

Summarizer Agent is an AI-powered tool designed to efficiently process and summarize documents. It automates the scanning of files from a designated folder, validates their format, and utlizes Groq API to generate concise, accurate summaries. The summaries are saved in a CSV file, streamlining document analysis for quicker insights.

## Features

- Automated File Processing: Automatically scans and processes files from a specified folder.
- File Validation: Ensures only valid formats are summarized.
- AI-Powered Summarization: Uses Groq’s advanced AI to deliver precise summaries.
- Bulk Processing: Simultaneously handles multiple files.
- Customizable Folder Path: Easily configure the folder path for input files.
- Error Handling: Provides feedback on any invalid or unsupported files.
- Efficient and Scalable: Optimized for processing large documents and multiple files efficiently.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/al-kafi-sohag/summarizer-agent.git
   cd summarizer-agent
   ```

2. Create a virtual environment and activate it:

   On Mac/Linux:

   ```sh
    python -m venv venv
    source venv/bin/activate
   ```

   On Windows:

   ```sh
    python -m venv venv
    venv\Scripts\activate
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Configure API Credentials:
   Edit the `config.yaml` file and add your API keys:
   ```yaml
   # Groq API Key: Obtain from https://groq.com
   groq_api_key: "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"
   ```

## Usage

1. Add documents to `data/` folder.

2. Run the `main.py` application:

   ```sh
   python main.py
   ```

3. Wait for the Summarization to Complete.

4. View the Results:
   Open the `result/` folder and locate `summary.csv` to review the summaries.

## Project Structure

- `config.yaml`: Stores configuration and API keys.
- `config_loader.yaml`: Loads project configurations.
- `main.py`: Core script that handles file processing and interaction with the summarizer agent.
- `summarizer.py`: Performs document summarization.
- `summary_saver.py`: Saves generated summaries to a CSV file.
- `data/`: Input folder for documents to be summarized.
- `result/`: Output folder containing the summary CSV files.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
