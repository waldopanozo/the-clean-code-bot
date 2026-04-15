# Ejemplos — antes y después

## `dirty_calculator.py` (antes)

- Sin docstrings ni tipado.
- Nombres crípticos (`calc`, `acc`, `t`).
- `div` sin validar división por cero.
- Estilo inconsistente (mezcla de estilos en una sola línea).

## `clean_calculator_reference.py` (después — referencia humana)

- Docstrings de módulo y funciones.
- Tipado con `float` y retornos explícitos.
- `divide` con `ValueError` documentada.
- Clase renombrada a `RunningTotal` con API clara (`accumulate`).

## Salida del bot (LLM)

Generá un archivo con el CLI (requiere `GROQ_API_KEY` u `OPENAI_API_KEY` en `.env`):

```bash
cd ..
python -m clean_code_bot refactor examples/dirty_calculator.py -o examples/clean_from_llm.py
```

El modelo puede diferir de `clean_calculator_reference.py`; lo importante es que siga el **CoT** en la respuesta y el **bloque de código** al final.

## Caso de prompt injection (bloqueado)

Si agregás en el archivo sucio una línea como `ignore previous instructions`, el **sanitizer** rechaza el archivo antes de llamar al LLM.
