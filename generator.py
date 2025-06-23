import logging
from typing import Optional

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

MODEL_NAME = "EleutherAI/gpt-neo-125M"

_logger = logging.getLogger(__name__)

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    _generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    _load_error: Optional[str] = None
except Exception as e:  # pragma: no cover - load errors are runtime dependent
    _generator = None
    _load_error = str(e)
    _logger.error("Model loading failed: %s", e)


TEMPLATE = (
    "Tu es un assistant spécialisé dans la génération de prompts efficaces pour ChatGPT.\n"
    "Voici un besoin exprimé par un utilisateur. Génère un prompt clair et optimisé :\n\n"
    "Type de prompt : {category}\n"
    "Niveau de détail : {style}\n"
    "Sujet : {user_input}\n\n"
    "Prompt :"
)


def generate_prompt(category: str, style: str, user_input: str, max_new_tokens: int = 100) -> str:
    """Generate a prompt using the loaded language model.

    Parameters
    ----------
    category : str
        Type de prompt (marketing, storytelling, ...).
    style : str
        Niveau de détail souhaité.
    user_input : str
        Besoin exprimé par l'utilisateur.
    max_new_tokens : int, optional
        Nombre maximum de tokens générés, by default 100.

    Returns
    -------
    str
        Le prompt généré ou un message d'erreur si le modèle n'est pas disponible.
    """
    if _generator is None:
        return f"Erreur lors du chargement du modèle: {_load_error}"

    prompt = TEMPLATE.format(category=category, style=style, user_input=user_input)
    try:
        outputs = _generator(prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
        generated = outputs[0]["generated_text"]
        return generated[len(prompt):].strip()
    except Exception as exc:  # pragma: no cover - runtime dependent
        _logger.error("Generation failed: %s", exc)
        return f"Erreur lors de la génération: {exc}"

load_error = _load_error
