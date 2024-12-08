# xampaperAnalyzer

xmpaperAnalyzer is a Python project designed to analyze exam question papers by extracting questions, categorizing them based on a provided syllabus, and analyzing trends across topics and subtopics. It converts JSON question data into a structured pandas DataFrame for further analysis, including generating leaderboards for frequent topics and subtopics.

## Features

- Extract questions from JSON data.
- Categorize questions based on a provided syllabus.
- Analyze trends in topics and subtopics.
- Generate leaderboards for frequent topics and subtopics.
- Save extracted data into CSV format for further processing.
- Keyword extraction using TF-IDF.
- Word cloud generation for visualizing focus areas.

## Prerequisites

- Python 3.7+
- Install required Python packages using the provided `requirements.txt` file.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/psypherion/xampaperAnalyzer.git
    cd xmpaperAnalyzer
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    - Create a `.env` file in the root directory.
    - Add your API key for Gemini as:
      ```
      GEMINI_API_KEY=your_api_key_here
      ```

## Usage

### Extract Questions and Analyze Topics

1. Place your syllabus JSON file and exam question JSON file in the project directory. Update the file paths in the script if necessary.

2. Run the `main.py` script:
    ```bash
    python main.py
    ```


## Contributing

Contributions are welcome! If you have suggestions or find a bug, feel free to open an issue or submit a pull request.

## License

This project is licensed under the Apache2 . See the `LICENSE` file for details.

## Contact

For any questions or feedback, please reach out to [psypherions@gmail.com].
