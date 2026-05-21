"""Настройки механизма связанных обращений.

Похожие заявки сравниваются только при совпадении category_id
(см. find_similar_tickets в linked_tickets.py).
"""

INACTIVE_STATUSES = frozenset({
    "completed",
    "closed",
    "archived",
})

# Порог 0.35 отсекал типичные пары вроде «не работает лифт» / «сломан лифт» (~0.31).
SIMILARITY_THRESHOLD = 0.25

SEARCH_WINDOW_DAYS = 30

# Искать по дому (улица + номер), а не только по точной квартире.
MATCH_SAME_BUILDING = True

PRIORITY_RULES = [
    {"min_subscribers": 1, "max_subscribers": 2, "priority": "medium"},
    {"min_subscribers": 3, "max_subscribers": 10, "priority": "high"},
    {"min_subscribers": 11, "max_subscribers": None, "priority": "urgent"},
]

STATUS_LABELS = {
    "new": "Новая",
    "in_progress": "В работе",
    "completed": "Завершена",
    "closed": "Закрыта",
    "archived": "Архивирована",
}
