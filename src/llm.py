import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"

# A function to call an LLM model and return the response
def call_llm_model(model_name, messages, temperature=1.0, top_p=1.0):
    """
    Call LLM model with messages
    
    Args:
        model_name: The model to use
        messages: List of message dictionaries with 'role' and 'content'
        temperature: Sampling temperature
        top_p: Top-p sampling parameter
    
    Returns:
        str: The model's response content
    """
    client = OpenAI(base_url=endpoint, api_key=token)
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        model=model_name
    )
    return response.choices[0].message.content

def translate_text(text, target_language, source_language="auto"):
    """
    Translate text to target language using LLM
    
    Args:
        text: The text to translate
        target_language: Target language (e.g., 'Chinese', 'English', 'Spanish')
        source_language: Source language (default: 'auto' for auto-detection)
    
    Returns:
        str: Translated text
    """
    if source_language == "auto":
        system_prompt = f"You are a professional translator. Translate the following text to {target_language}. Only return the translated text without any explanations or additional comments."
    else:
        system_prompt = f"You are a professional translator. Translate the following text from {source_language} to {target_language}. Only return the translated text without any explanations or additional comments."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    
    try:
        translated = call_llm_model(model, messages, temperature=0.3, top_p=0.9)
        return translated.strip()
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

def translate_note(title, content, target_language):
    """
    Translate both title and content of a note
    
    Args:
        title: Note title
        content: Note content
        target_language: Target language
    
    Returns:
        dict: Dictionary with 'title' and 'content' keys containing translations
    """
    try:
        translated_title = translate_text(title, target_language)
        translated_content = translate_text(content, target_language)
        
        return {
            "title": translated_title,
            "content": translated_content
        }
    except Exception as e:
        raise Exception(f"Note translation failed: {str(e)}")