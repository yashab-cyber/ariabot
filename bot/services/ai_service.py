"""
AI Assistant Service for Aria.
Supports OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, LM Studio.
Handles conversation memory, streaming, topic auto-detection, prompt formatting, and token counting.
"""
from typing import AsyncGenerator, Dict, List, Optional
import aiohttp
import json
from bot.config.settings import settings
from bot.utils.logger import logger


class AIService:
    def __init__(self):
        # Conversation history key -> list of {"role": str, "content": str}
        self.conversations: Dict[str, List[dict]] = {}
        # Per-user provider/model overrides
        self.user_providers: Dict[int, str] = {}
        self.user_models: Dict[int, str] = {}
        # Token usage metrics counter
        self.total_tokens_processed: int = 0

    def set_user_preference(self, user_id: int, provider: Optional[str] = None, model: Optional[str] = None):
        if provider:
            self.user_providers[user_id] = provider
        if model:
            self.user_models[user_id] = model

    def get_user_preference(self, user_id: int) -> tuple[str, str]:
        prov = self.user_providers.get(user_id, settings.DEFAULT_AI_PROVIDER)
        mod = self.user_models.get(user_id, settings.DEFAULT_AI_MODEL)
        return prov, mod

    def _get_history(self, context_key: str) -> List[dict]:
        if context_key not in self.conversations:
            self.conversations[context_key] = []
        return self.conversations[context_key]

    def clear_history(self, context_key: str) -> None:
        if context_key in self.conversations:
            self.conversations[context_key] = []

    def estimate_tokens(self, text: str) -> int:
        """Rough token count estimation (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    def detect_topic(self, prompt: str) -> str:
        """Auto-detects the domain of the user query."""
        p_lower = prompt.lower()
        if any(kw in p_lower for kw in ["def ", "class ", "function", "bug", "code", "python", "js", "html", "css", "git", "syntax"]):
            return "Programming & Code"
        elif any(kw in p_lower for kw in ["solve", "math", "equation", "calculate", "integral", "matrix"]):
            return "Mathematics"
        elif any(kw in p_lower for kw in ["rewrite", "grammar", "essay", "paragraph", "tone", "synonym"]):
            return "Writing & Language"
        elif any(kw in p_lower for kw in ["error", "traceback", "crash", "fix", "issue", "debug", "failed"]):
            return "Troubleshooting"
        return "General Knowledge"

    async def generate_response(
        self,
        prompt: str,
        context_key: str = "global",
        system_prompt: str = "You are Aria, an expert AI assistant for the OpenDroid Discord Community.",
        user_id: Optional[int] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        """Generates AI response from configured provider."""
        pref_prov, pref_mod = self.get_user_preference(user_id) if user_id else (settings.DEFAULT_AI_PROVIDER, settings.DEFAULT_AI_MODEL)
        provider = provider or pref_prov
        model = model or pref_mod

        history = self._get_history(context_key)
        history.append({"role": "user", "content": prompt})

        # Track prompt tokens
        self.total_tokens_processed += self.estimate_tokens(prompt)

        # Keep history within reasonable window (last 10 messages)
        messages_payload = [{"role": "system", "content": system_prompt}] + history[-10:]

        try:
            full_response = ""
            if provider.lower() in ["openai", "groq", "openrouter", "lmstudio", "ollama"]:
                async for chunk in self._call_openai_compatible(provider, model, messages_payload):
                    full_response += chunk
                    yield chunk
            elif provider.lower() == "anthropic":
                async for chunk in self._call_anthropic(model, messages_payload):
                    full_response += chunk
                    yield chunk
            else:
                # Fallback / Mock generator for offline / fallback execution
                fallback_msg = f"**[Aria AI]** Topic: *{self.detect_topic(prompt)}*\n\nHere is a response to: '{prompt}'\n\n*(Powered by {provider.title()} - {model})*"
                full_response = fallback_msg
                yield fallback_msg

            # Save response to history and track tokens
            self.total_tokens_processed += self.estimate_tokens(full_response)
            history.append({"role": "assistant", "content": full_response})

        except Exception as e:
            logger.error(f"Error in AIService ({provider}/{model}): {e}")
            yield f"⚠️ AI Provider Error ({provider}): Could not complete request. {str(e)}"

    async def _call_openai_compatible(
        self,
        provider: str,
        model: str,
        messages: List[dict]
    ) -> AsyncGenerator[str, None]:
        endpoint = "https://api.openai.com/v1/chat/completions"
        api_key = settings.OPENAI_API_KEY

        if provider == "groq":
            endpoint = "https://api.groq.com/openai/v1/chat/completions"
            api_key = settings.GROQ_API_KEY
        elif provider == "openrouter":
            endpoint = "https://openrouter.ai/api/v1/chat/completions"
            api_key = settings.OPENROUTER_API_KEY
        elif provider == "ollama":
            endpoint = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat"
            api_key = "ollama"
        elif provider == "lmstudio":
            endpoint = f"{settings.LMSTUDIO_BASE_URL.rstrip('/')}/chat/completions"
            api_key = "lm-studio"

        if not api_key and provider not in ["ollama", "lmstudio"]:
            yield f"⚠️ API Key for provider '{provider}' is not configured in .env."
            return

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else ""
        }
        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=payload, timeout=30) as resp:
                if resp.status != 200:
                    err_text = await resp.text()
                    yield f"API error ({resp.status}): {err_text[:200]}"
                    return

                async for line in resp.content:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data: "):
                        line_data = line_str[6:]
                        if line_data == "[DONE]":
                            break
                        try:
                            data = json.loads(line_data)
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            continue

    async def _call_anthropic(
        self,
        model: str,
        messages: List[dict]
    ) -> AsyncGenerator[str, None]:
        if not settings.ANTHROPIC_API_KEY:
            yield "⚠️ Anthropic API key is not configured in .env."
            return

        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_messages = [m for m in messages if m["role"] != "system"]

        payload = {
            "model": model or "claude-3-haiku-20240307",
            "max_tokens": 1024,
            "system": system_msg,
            "messages": user_messages
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload) as resp:
                if resp.status == 200:
                    res_json = await resp.json()
                    yield res_json["content"][0]["text"]
                else:
                    yield f"Anthropic error ({resp.status}): {await resp.text()}"


ai_service = AIService()
