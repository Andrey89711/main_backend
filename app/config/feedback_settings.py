"""Настройки обратной связи и оспаривания заявок."""

FEEDBACK_TYPES = frozenset({
    "review",
    "dispute",
})

FEEDBACK_TYPE_LABELS = {
    "review": "Отзыв",
    "dispute": "Оспаривание",
}

# Статусы, в которых жилец может оставить обратную связь.
FEEDBACK_ALLOWED_STATUSES = frozenset({
    "completed",
    "auto_closed",
})

STATUS_AFTER_POSITIVE_FEEDBACK = "closed"

STATUS_AFTER_DISPUTE = "dispute_review"

# Срок (дней) ожидания обратной связи после «Выполнена».
AUTO_CLOSE_FEEDBACK_DAYS = 7

STATUS_AFTER_AUTO_CLOSE = "auto_closed"
