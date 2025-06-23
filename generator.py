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

PROMPT_TEMPLATES = {
    "Agis comme...": (
        "Tu dois générer un prompt commençant par 'Agis comme...'.\n"
        "Réponds en français.\n"
        "{category_instruction}\n"
        "{style_instruction}\n"
        "Demande de l'utilisateur : {user_input}\n\n"
        "Formule le prompt final à coller dans ChatGPT :"
    ),
    "Étapes à suivre": (
        "Tu dois générer un prompt demandant une réponse étape par étape.\n"
        "Réponds en français.\n"
        "{category_instruction}\n"
        "{style_instruction}\n"
        "Demande de l'utilisateur : {user_input}\n\n"
        "Écris le prompt final à coller dans ChatGPT :"
    ),
    "Objectif clair": (
        "Tu dois générer un prompt centré sur un objectif explicite.\n"
        "Réponds en français.\n"
        "{category_instruction}\n"
        "{style_instruction}\n"
        "Objectif exprimé : {user_input}\n\n"
        "Écris le prompt final à coller dans ChatGPT :"
    ),
    "Réponse avec contraintes": (
        "Tu dois générer un prompt qui impose des contraintes de format, ton, ou longueur.\n"
        "Réponds en français.\n"
        "{category_instruction}\n"
        "{style_instruction}\n"
        "Contrainte exprimée : {user_input}\n\n"
        "Écris le prompt final à coller dans ChatGPT :"
    ),
    "Créatif / roleplay": (
        "Tu dois générer un prompt immersif ou créatif, avec un ton original ou un rôle imaginaire.\n"
        "Réponds en français.\n"
        "{category_instruction}\n"
        "{style_instruction}\n"
        "Idée exprimée : {user_input}\n\n"
        "Écris le prompt final à coller dans ChatGPT :"
    ),
}

def generate_prompt(category: str, style: str, pattern: str, user_input: str, max_new_tokens: int = 300) -> str:
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

    template = PROMPT_TEMPLATES.get(pattern)
    prompt = template.format(
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
        return result.strip()
    except Exception as exc:
        _logger.error("Erreur génération API Hugging Face : %s", exc)
        return f"Erreur lors de la génération : {exc}"

load_error = _load_error
