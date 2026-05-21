import re
from difflib import SequenceMatcher


STOP_WORDS = frozenset({
    "и", "в", "на", "не", "что", "по", "из", "за", "до", "от", "как",
    "это", "для", "при", "уже", "или", "но", "а", "же", "ли", "бы",
    "the", "a", "an", "is", "are", "was", "were", "to", "of", "in",
})


def normalize_text(text: str) -> str:

    lowered = text.lower().strip()

    return re.sub(
        r"\s+",
        " ",
        lowered
    )


def extract_keywords(text: str) -> set[str]:

    tokens = re.findall(
        r"[а-яёa-z0-9]{3,}",
        normalize_text(text),
        flags=re.IGNORECASE
    )

    return {
        token
        for token in tokens
        if token not in STOP_WORDS
    }


def keyword_overlap_score(
    text_a: str,
    text_b: str
) -> float:

    keywords_a = extract_keywords(text_a)
    keywords_b = extract_keywords(text_b)

    if not keywords_a or not keywords_b:
        return 0.0

    intersection = keywords_a & keywords_b
    union = keywords_a | keywords_b

    return len(intersection) / len(union)


def sequence_similarity(
    text_a: str,
    text_b: str
) -> float:

    normalized_a = normalize_text(text_a)
    normalized_b = normalize_text(text_b)

    if not normalized_a or not normalized_b:
        return 0.0

    return SequenceMatcher(
        None,
        normalized_a,
        normalized_b
    ).ratio()


def shared_keyword_ratio(
    text_a: str,
    text_b: str
) -> float:

    """Доля значимых слов из более короткого текста, встречающихся во втором."""

    keywords_a = extract_keywords(text_a)
    keywords_b = extract_keywords(text_b)

    if not keywords_a or not keywords_b:
        return 0.0

    norm_a = normalize_text(text_a)
    norm_b = normalize_text(text_b)

    if len(keywords_a) <= len(keywords_b):
        shorter, longer_text = keywords_a, norm_b
    else:
        shorter, longer_text = keywords_b, norm_a

    hits = sum(
        1
        for token in shorter
        if token in longer_text
    )

    return hits / len(shorter)


def combined_similarity(
    text_a: str,
    text_b: str
) -> float:

    keyword_score = keyword_overlap_score(
        text_a,
        text_b
    )

    sequence_score = sequence_similarity(
        text_a,
        text_b
    )

    shared_score = shared_keyword_ratio(
        text_a,
        text_b
    )

    return max(
        keyword_score,
        sequence_score,
        shared_score,
        (keyword_score + sequence_score) / 2
    )
