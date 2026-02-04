from word2number import w2n
from number_parser import parse_number


def extract_number(user_input):
    """
    Extracts a valid integer from raw user input.
    
    First attempts to find digits in the input. If none are found,
    tries to parse word-based numbers (e.g., "twenty five" -> 25).
    
    Args:
        user_input (str): Raw user input string
        
    Returns:
        int: The extracted number
        
    Raises:
        ValueError: If no valid number can be extracted from the input
    """
    # Try to extract digits directly
    digits = [int(s) for s in user_input.split() if s.isdigit()]
    
    if digits:
        return digits[0]
    
    # Fall back to word-based number parsing
    try:
        cleaned_data = user_input.lower().replace("-", " ")
        cleaned_data = cleaned_data.replace(".", "")
        
        number = parse_number(cleaned_data)
        return w2n.word_to_num(number)
    except ValueError:
        raise ValueError(f"No valid number found in input: {user_input}")

