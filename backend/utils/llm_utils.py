import ollama


semantic_groups = {
    "credit": [
        "Credit reporting, credit repair services, or other personal consumer reports",
        "Credit reporting",
    ],
    "money_transfer": [
        "Money transfer, virtual currency, or money service",
        "Money transfers",
    ],
    "card": ["Credit card", "Credit card or prepaid card", "Prepaid card"],
    "loan": [
        "Student loan",
        "Consumer Loan",
        "Vehicle loan or lease",
        "Payday loan, title loan, or personal loan",
        "Payday loan",
    ],
}


def build_llm_prompt(row, category_cols, tags_list):
    """
    Constructs a prompt for a Large Language Model to categorize a customer complaint.

    :param row: A dictionary-like object (e.g., a pandas Series) containing the complaint data.
    :param category_cols: A list of column names to include as metadata in the prompt.
    :param tags_list: A list or string representation of valid tags for categorization.
    :return: A formatted string containing the system role, task instructions,
             metadata, complaint text, and the list of allowed tags.
    """

    metadata = "\n".join([f"- {col}: {row[col]}" for col in category_cols])

    numbered_tags = "\n".join([f"{i}. {tag}" for i, tag in enumerate(tags_list)])

    prompt = f"""    
ROLE: You are a highly precise Customer Support Classifier. Your sole purpose is to map customer complaints to a specific predefined tag.

INSTRUCTION :
Analyze the customer complaint and select the most appropriate tag number from the list below.

CONSTRAINTS :
- Output ONLY the tag tex.
- Output must EXACTLY macth one tag number from the list.
- No explanations, no punctuation, no extra words.
- If unsure, pick the closest tag number.
- Never invent a new tag number.

ALLOWED TAGS LIST :
{numbered_tags}

COMPLAINT DETAILS : 
{metadata}
- Consumer Claim : {row['Consumer Claim']}
- Company : {row['Company']}
- State : {row['State']}
- ZIP Code : {row['ZIP code']}

IMPORTANT :
Before answering, internally verify that your output is in the list.

ANSWER :"""

    return prompt


def parse_llm_output(output, tags_list):
    """
    Parses the LLM's raw output to extract a valid tag from the provided list.

    :param output: The raw string response from the LLM.
    :param tags_list: The list of valid tags corresponding to the indices.
    :return: The tag string if a valid index is found, otherwise None.
    """
    try:
        index = int(output.strip())
        if 0 <= index < len(tags_list):
            return tags_list[index]
    except:
        pass

    return None


def query_llm(prompt, tags_list, model="mistral:7b", max_retry=2):
    """
    Sends a prompt to the LLM and attempts to parse a valid tag from the response.

    :param prompt: The formatted prompt string to send to the model.
    :param tags_list: The list of allowed tags for validation.
    :param model: The name of the model to use (default "mistral:7b").
    :param max_retry: Number of attempts to get a valid parseable response.
    :return: A tuple containing (parsed_tag, raw_response).
    """
    for _ in range(max_retry):
        try:
            response = ollama.generate(model=model, prompt=prompt)
            raw = response["response"].strip()
            parsed = parse_llm_output(raw, tags_list)

            if parsed:
                return parsed, raw
        except Exception as e:
            raw = f"Error: {str(e)}"

    return "UNKNOWN", raw


def same_group(label1, label2):
    for group in semantic_groups.values():
        if label1 in group and label2 in group:
            return True

    return False


def semantic_accuracy(dataframe):
    correct = 0

    for _, row in dataframe.iterrows():
        if row["ollama_pred"] == row["true_label"]:
            correct += 1
        elif same_group(row["ollama_pred"], row["true_label"]):
            correct += 1

    return correct / len(dataframe)
