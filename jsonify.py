import re
import json

# Read the content of the output.txt file
with open("output.txt", "r") as file:
    content = file.read()

# Regular expression to extract JSON data inside ```json ... ```
pattern = r"```json\n(.*?)\n```"

# Find all matches (use re.DOTALL to handle multiline JSON)
matches = re.findall(pattern, content, re.DOTALL)

# Assuming there is only one JSON block or you want the first one
if matches:
    json_data = matches[0]
    try:
        # Parse the extracted string as JSON
        parsed_json = json.loads(json_data)

        # Save to a new JSON file
        with open("output.json", "w") as json_file:
            json.dump(parsed_json, json_file, indent=4)

        print("JSON data extracted and saved successfully.")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
else:
    print("No JSON data found in the file.")
