# xmpaperAnalyzer

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
    git clone https://github.com/your-username/xmpaperAnalyzer.git
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

3. The script will:
    - Extract questions from the JSON file.
    - Categorize questions into topics and subtopics based on the syllabus.
    - Generate a pandas DataFrame.
    - Save the DataFrame to a CSV file (`questions_output.csv`).

4. View the leaderboard for the most frequent topics and subtopics directly in the console.

### Generate Word Cloud

To visualize the focus areas:

1. Modify the script to call the `extract_keywords` function with a list of questions.
2. Run the script, and a word cloud will be displayed.

## Example

### Input JSON (Question Data)
```json
[
    {
        "questions": [
            {
                "question_no": 1,
                "question": "What is AI?",
                "options": {
                    "a": "Artificial Intelligence",
                    "b": "Adobe Illustrator",
                    "c": "Automated Input",
                    "d": "None"
                },
                "answer": "a",
                "explanation": "AI refers to Artificial Intelligence.",
                "category": {
                    "unit": "AI Basics",
                    "topic": "Introduction"
                }
            }
        ]
    }
]
```

### Output CSV
| question_no | question      | option_a                 | option_b             | option_c       | option_d | answer | explanation                       | unit      | topic        |
|-------------|---------------|--------------------------|----------------------|----------------|----------|--------|-----------------------------------|-----------|--------------|
| 1           | What is AI?   | Artificial Intelligence | Adobe Illustrator   | Automated Input | None     | a      | AI refers to Artificial Intelligence. | AI Basics | Introduction |

## Contributing

Contributions are welcome! If you have suggestions or find a bug, feel free to open an issue or submit a pull request.

## License

This project is licensed under the Apache2 . See the `LICENSE` file for details.

## Contact

For any questions or feedback, please reach out to [psypherions@gmail.com].
