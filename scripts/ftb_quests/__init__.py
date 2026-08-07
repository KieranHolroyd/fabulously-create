"""Fabulously Create FTB Quests book definitions (AST)."""
from __future__ import annotations

from .ast import Book
from .chapters import all_chapters
from .connections import wire_connections
from .editorial import polish_book
from .intro import add_chapter_intros


def build_book() -> Book:
    """Build the quest book AST, then wire visible cross-chapter connections."""
    book = polish_book(Book(chapters=all_chapters()))
    book = add_chapter_intros(book)
    return wire_connections(book)
