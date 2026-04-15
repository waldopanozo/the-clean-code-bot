class Calculadora:
    def __init__(self):
        """Inicializa la calculadora con un total de 0."""
        self.total = 0

    def acumular(self, valor: float) -> float:
        """Acumula un valor en el total."""
        self.total += valor
        return self.total

    def __str__(self) -> str:
        """Devuelve una representación legible de la calculadora."""
        return f"Calculadora con total {self.total}"

def suma(a: float, b: float) -> float:
    """Devuelve la suma de dos números."""
    return a + b

def resta(a: float, b: float) -> float:
    """Devuelve la resta de dos números."""
    return a - b

def multiplicacion(a: float, b: float) -> float:
    """Devuelve la multiplicación de dos números."""
    return a * b

def division(a: float, b: float) -> float:
    """Devuelve la división de dos números."""
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b