import requests
import json
import base64
from typing import List, Dict, Optional, Any, Union
from datetime import datetime

# Define the fields we want to extract from images with their data types
EXTRACTABLE_FIELDS = {
    "title": str,
    "description": str,
    "date": str,  # Expected format: YYYY-MM-DD
    "time": str,  # Expected format: HH:MM
    "venue": str,
    "capacity": int,
    "isPaid": bool,
    "price": {
        "value": float,
        "currency": str
    }
}

class OllamaService:
    def __init__(self, host: str = "http://localhost:11434"):
        """Initialize Ollama service with host URL"""
        self.base_url = host
        self.model = "llava"  # Default model for image processing
    
    def _make_request(self, endpoint: str, payload: dict) -> dict:
        """Make a POST request to Ollama API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to communicate with Ollama: {str(e)}")

    def _validate_and_convert_type(self, field: str, value: Any) -> Any:
        """Validate and convert the value to the expected type"""
        if value is None:
            return None
            
        expected_type = EXTRACTABLE_FIELDS[field]
        try:
            if field == "price":
                if isinstance(value, dict):
                    return {
                        "value": float(value.get("value", 0)),
                        "currency": str(value.get("currency", ""))
                    }
                return {
                    "value": float(value) if value else 0,
                    "currency": "USD"  # default currency
                }
            elif field == "date":
                # Attempt to parse and standardize date format
                if isinstance(value, str) and value:
                    try:
                        parsed_date = datetime.strptime(value, "%Y-%m-%d")
                        return parsed_date.strftime("%Y-%m-%d")
                    except ValueError:
                        return None
                return None
            elif field == "time":
                # Attempt to parse and standardize time format
                if isinstance(value, str) and value:
                    try:
                        parsed_time = datetime.strptime(value, "%H:%M")
                        return parsed_time.strftime("%H:%M")
                    except ValueError:
                        return None
                return None
            elif expected_type == bool:
                if isinstance(value, str):
                    return value.lower() in ['true', 'yes', '1']
                return bool(value)
            elif expected_type == int:
                try:
                    # Remove any non-numeric characters except digits
                    cleaned_value = ''.join(filter(str.isdigit, str(value)))
                    return int(cleaned_value) if cleaned_value else None
                except ValueError:
                    return None
            else:
                return expected_type(value) if value else None
        except (ValueError, TypeError):
            return None

    def _extract_json_from_text(self, text: str) -> dict:
        """Extract valid JSON from text response by finding the first { and last }"""
        try:
            # Find the first { and last } to extract potential JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end != 0:
                potential_json = text[start:end]
                return json.loads(potential_json)
            return {}
        except json.JSONDecodeError:
            # If still can't parse, try to find individual key-value pairs
            extracted_data = {}
            for field in EXTRACTABLE_FIELDS.keys():
                # Look for field in format "field": value or "field":"value"
                field_pattern = f'"{field}":\\s*([^,}}]+)'
                import re
                match = re.search(field_pattern, text)
                if match:
                    value = match.group(1).strip().strip('"')
                    if value.lower() != 'null':
                        extracted_data[field] = value
            return extracted_data

    def get_image_extract(self, image_base64: str, caption: str = "") -> Dict[str, Any]:
        """
        Extract information from an image using Ollama's vision model
        
        Args:
            image_base64: Base64 encoded image string
            caption: Optional caption or context about the image
        
        Returns:
            Dictionary containing extracted fields and their values with proper types
        """
        prompt = f"""
        Analyze this image{f' of {caption}' if caption else ''} and extract the following event information if visible:
        
        Required fields and their expected formats:
        - title (text): The event title or name
        - description (text): Brief description of the event
        - date (YYYY-MM-DD format): The event date
        - time (HH:MM format): The event time
        - venue (text): Location or venue name
        - capacity (number): Maximum number of attendees
        - isPaid (boolean): Whether the event requires payment
        - price: {{"value": number, "currency": text}}: Event cost if paid
        
        Please respond in a JSON format with these fields. Use null for fields that cannot be determined from the image.
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False
        }

        try:
            response = self._make_request("generate", payload)
            
            # Extract JSON data from response text
            extracted_data = self._extract_json_from_text(response['response'])
            
            # Validate and convert types for each field, only keeping non-None values
            validated_data = {}
            for field in EXTRACTABLE_FIELDS.keys():
                if field in extracted_data:
                    value = self._validate_and_convert_type(field, extracted_data[field])
                    if value is not None:  # Only include non-None values
                        validated_data[field] = value
            
            return validated_data

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return {}  # Return empty dict instead of null fields

    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
