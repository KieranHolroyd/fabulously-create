"""Fabulously Create FTB Quests book definitions (AST)."""
from __future__ import annotations

from .ast import Book
from .chapters import all_chapters
from .connections import wire_connections


def build_book() -> Book:
    """Build the quest book AST, then wire visible cross-chapter connections."""
    return wire_connections(Book(chapters=all_chapters()))