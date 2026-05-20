"""
Таблица рекордов: сохранение и загрузка из JSON
"""

import json
import os
from typing import List, Dict


class Leaderboard:
    """Управление таблицей рекордов (топ-10)"""

    def __init__(self, filename: str = "leaderboard.json"):
        self._filename = filename
        self._records: List[Dict] = []
        self._load()

    def _load(self) -> None:
        """Загружает рекорды из JSON файла"""
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._records = data.get("records", [])
            except (json.JSONDecodeError, IOError):
                self._records = []

    def _save(self) -> None:
        """Сохраняет рекорды в JSON файл"""
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump({"records": self._records}, f, ensure_ascii=False, indent=2)

    def add_record(self, nickname: str, score: int, map_type: str) -> bool:
        """Добавляет новый рекорд."""
        record = {
            "nickname": nickname,
            "score": score,
            "map_type": map_type
        }
        self._records.append(record)

        # Сортируем по убыванию очков
        self._records.sort(key=lambda x: x["score"], reverse=True)

        # Оставляем только топ-10
        if len(self._records) > 10:
            self._records = self._records[:10]

        self._save()

        return record in self._records

    def get_top_scores(self, limit: int = 10) -> List[Dict]:
        """Возвращает топ-N рекордов"""
        return self._records[:limit]

    def is_new_record(self, score: int) -> bool:
        """Проверяет, является ли счёт рекордным"""
        if len(self._records) < 10:
            return True

        return score > self._records[-1]["score"]
