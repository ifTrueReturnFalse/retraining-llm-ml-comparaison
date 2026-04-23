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

    prompt = f"""
### INSTRUCTION
Analyze the customer complaint and select the most appropriate tag from the list below.
    
### ALLOWED TAGS LIST :
{"\n".join(tags_list)}

### ROLE: You are a highly precise Customer Support Classifier. Your sole purpose is to map customer complaints to a specific predefined tag.

### CONSTRAINTS :
- YOUR RESPONSE MUST CONTAIN ONLY THE TAG NAME.
- NO PUNCTUATION, NO EXPLANATIONS, NO INTRODUCTIONS.
- IF THE COMPLAINT IS UNCLEAR, CHOOSE THE MOST LIKELY TAG.
- THE TAG MUST BE SELECTED FROM THE PROVIDED LIST BELOW.

### COMPLAINT CONTEXT : 
{metadata}

### COMPLAINT DETAILS : 
- Consumer Claim : {row['Consumer Claim']}
- Company : {row['Company']}
- State : {row['State']}
- ZIP Code : {row['ZIP code']}


### RESPONSE
Tag:"""
    
    return prompt