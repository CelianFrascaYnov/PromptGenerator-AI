import logging
from typing import Optional
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
_logger = logging.getLogger(__name__)

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

try:
    client = InferenceClient(model=MODEL_NAME, token=HUGGINGFACE_TOKEN)
    _load_error: Optional[str] = None
except Exception as e:
    client = None
    _load_error = str(e)
    _logger.error("Client HuggingFace non initialisé : %s", e)

TEMPLATE = (
    "Tu es un générateur de prompts pour ChatGPT. "
    "Ta tâche est de produire un prompt clair, structuré et directement utilisable dans ChatGPT, "
    "en respectant les instructions suivantes :\n\n"
    "- Tu dois répondre en français\n"
    "- {category_instruction}\n"
    "- {style_instruction}\n\n"
    "Voici la demande de l'utilisateur : {user_input}\n\n"
    "Formule uniquement le prompt final à copier-coller dans ChatGPT, sans explication autour :"
)

def generate_prompt(category: str, style: str, user_input: str, max_new_tokens: int = 30000) -> str:
    if client is None:
        return f"Erreur lors de l'initialisation du client HF : {_load_error}"

    category_instruction = {
        "Marketing": "Tu es un expert en marketing digital. Tu aides à formuler des prompts pour générer des campagnes ou des stratégies persuasives.",
        "Storytelling": "Tu es un écrivain créatif. Tu formules des prompts qui inspirent des histoires engageantes ou immersives.",
        "Code": "Tu es un ingénieur logiciel expert. Tu formules des prompts permettant de générer du code clair, documenté et fonctionnel.",
        "Étude": "Tu es un professeur expérimenté. Tu formules des prompts pour expliquer, résumer ou interroger sur des concepts académiques.",
    }.get(category, "")

    style_instruction = {
        "Simple": "Le prompt doit être court, direct, et sans détails inutiles.",
        "Moyen": "Le prompt doit inclure une consigne claire et un peu de contexte.",
        "Très détaillé": "Le prompt doit inclure un rôle explicite, un objectif précis, un contexte et des contraintes.",
    }.get(style, "")

    prompt = TEMPLATE.format(
        category_instruction=category_instruction,
        style_instruction=style_instruction,
        user_input=user_input,
    )

    try:
        result = client.text_generation(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.15,
        )
        generated = result.strip()

        # Post-traitement : isole uniquement le prompt généré
        if "Prompt généré :" in generated:
            generated = generated.split("Prompt généré :", 1)[-1].strip()
        return generated
    except Exception as exc:
        _logger.error("Erreur génération API Hugging Face : %s", exc)
        return f"Erreur lors de la génération : {exc}"

load_error = _load_error
