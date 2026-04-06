from persistent import json
import re

logger = logging.getLogger(__name__)

def is_persona_out(state:State):

    """
    是否是人设输出
    """
    self_keywords = json.all_json.get("PERSONA_ABOUT_WORDS").get("self_keywords")
    regex_patterns = json.all_json.get("PERSONA_ABOUT_WORDS").get("regex_patterns")
    blacklist_keywords = json.all_json.get("PERSONA_ABOUT_WORDS").get("blacklist_keywords")
    characters = json.all_json.get("PERSONA_ABOUT_WORDS").get("characters")

    current_message = state["query"].strip().lower()
    compiled_patterns = [re.compile(p, re.I) for p in regex_patterns]

    has_characters = any(character in current_message for character in characters)
    has_self_keywords = any(keyword in current_message for keyword in self_keywords)
    has_regex_patterns = any(p.search(current_message) for p in compiled_patterns)
    has_blacklist_keywords = any(k in current_message for k in blacklist_keywords)

    logger.info(f"has_characters: {has_characters}, has_self_keywords: {has_self_keywords}, has_regex_patterns: {has_regex_patterns}, has_blacklist_keywords: {has_blacklist_keywords}")

    return {"judgment": has_characters or ((has_self_keywords or has_regex_patterns) and not has_blacklist_keywords)}

