"""AI Suggestion Service for home remedies."""
import httpx
from typing import Optional
from app.config import settings


class AISuggestionService:
    """Service to get AI-powered home remedy suggestions."""
    
    # Using HuggingFace's OpenAI-compatible API endpoint
    HUGGINGFACE_API_URL = "https://router.huggingface.co/v1/chat/completions"
    # Default model - a supported chat model on HF Inference
    DEFAULT_MODEL = "HuggingFaceTB/SmolLM3-3B:hf-inference"
    
    @staticmethod
    async def get_home_remedies(illness_name: str, notes: Optional[str] = None) -> Optional[str]:
        """Get home remedy suggestions for an illness using Hugging Face API."""
        try:
            description = illness_name
            if notes:
                description += f". Additional details: {notes}"
            
            system_prompt = "You are a helpful health assistant. Provide safe, practical home remedies. Always recommend consulting a doctor for serious symptoms."
            
            user_prompt = f"""A person is experiencing: {description}

Please provide 3-5 simple home remedies or tips that could help. Keep it brief and practical. Only suggest safe, common remedies like rest, hydration, etc.

Also, don't write the response as If you are thinking: write it in the style as if it is a general tips and tricks that someone might be giving to either his friend or relative.

Format your response as a simple numbered list."""

            headers = {
                "Content-Type": "application/json",
            }
            
            # Add API key if configured
            if settings.huggingface_api_key:
                headers["Authorization"] = f"Bearer {settings.huggingface_api_key}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    AISuggestionService.HUGGINGFACE_API_URL,
                    headers=headers,
                    json={
                        "model": AISuggestionService.DEFAULT_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "max_tokens": 300,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result and "choices" in result and len(result["choices"]) > 0:
                        content = result["choices"][0]["message"]["content"].strip()
                        # Remove thinking tags and markdown asterisks
                        content = content.replace("<think>", "").replace("</think>", "")
                        content = content.replace("**", "")
                        return content
                
                # Log error but don't fail the illness creation
                print(f"AI suggestion API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            # Log error but don't fail the illness creation
            print(f"AI suggestion error: {str(e)}")
            return None
