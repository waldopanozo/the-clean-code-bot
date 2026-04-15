"""
Referencia manual de "después" (sin LLM) para comparar con la salida del bot.

Muestra: docstrings, tipado, SRP (operaciones separadas), validación en división.
"""

from __future__ import annotations


def add(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Resta b de a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Producto de a y b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Cociente de a entre b. Lanza ValueError si b es cero."""
    if b == 0:
        raise ValueError("El divisor no puede ser cero.")
    return a / b


class RunningTotal:
    """Acumulador simple compatible con el ejemplo sucio original."""

    def __init__(self) -> None:
        self._total: float = 0.0

    def accumulate(self, value: float) -> float:
        """Suma value al total y devuelve el total actual."""
        self._total += value
        return self._total
