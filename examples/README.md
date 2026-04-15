# Ejemplos — antes y después

Repositorio del proyecto: [github.com/waldopanozo/the-clean-code-bot](https://github.com/waldopanozo/the-clean-code-bot).

Este archivo amplía el **[README principal](../README.md)** (sección *Ejemplos y evidencia de uso*): acá están las tablas de corrida, los nombres de archivos y los comandos copiables.

## Registro de ejecución (evidencia local)

Sesión típica en **PowerShell**, directorio de trabajo: `D:\Assure\MOODLE\clean-code-bot`, entorno **`.venv`** activado (`(.venv)` en el prompt). Resumen:

| Paso | Comando o acción | Resultado observado |
|------|------------------|----------------------|
| 1 | `python -m venv .venv` | Creada la carpeta del entorno virtual. |
| 2 | `.\.venv\Scripts\Activate.ps1` | Prompt con prefijo `(.venv)`; `pip` apunta al venv. |
| 3 | `pip install -r requirements.txt` | Instalación correcta de `click`, `openai`, `python-dotenv` y dependencias transitivas. |
| 4 | `python -m pip --version` | Confirmación: `pip ... from ...\clean-code-bot\.venv\...` (Python 3.13 en la captura). |
| 5 | `copy .env.example .env` | Archivo `.env` creado para pegar la API key (no versionar). |
| 6 | `python -m clean_code_bot refactor examples\dirty_calculator.py --dry-run` | Salida completa del modelo: secciones **1–4** del CoT (Markdown) + bloque ` ```python ` con una propuesta de refactor (útil para revisar el razonamiento). |
| 7 | `python -m clean_code_bot refactor examples\dirty_calculator.py -o examples\clean_from_llm.py` | Mensaje: `Escrito: examples\clean_from_llm.py` y el **código final** solo en ese archivo (bloque extraído; puede diferir de la corrida `--dry-run` porque el LLM no es determinista). |

**Archivos del ejemplo usados en la sesión:**

| Rol | Ruta |
|-----|------|
| Entrada (“antes”) | `examples/dirty_calculator.py` |
| Salida del script (LLM) | `examples/clean_from_llm.py` |
| Referencia humana (“después” ideal) | `examples/clean_calculator_reference.py` |

**Nota:** En el README principal, los comandos de `Set-Location` / `cd` usan una **ruta de ejemplo**; sustituila por la carpeta real donde tengas el clon (en la sesión registrada fue `D:\Assure\MOODLE\clean-code-bot`).

---

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

Desde la raíz del repo `clean-code-bot/` (con venv activado y `.env` configurado):

**Windows (PowerShell):**

```powershell
python -m clean_code_bot refactor examples\dirty_calculator.py -o examples\clean_from_llm.py
```

**Linux / macOS:**

```bash
python -m clean_code_bot refactor examples/dirty_calculator.py -o examples/clean_from_llm.py
```

Requiere `GROQ_API_KEY` u `OPENAI_API_KEY` en `.env`.

El modelo puede diferir de `clean_calculator_reference.py`; lo importante es que siga el **CoT** en la respuesta y el **bloque de código** al final.

## Caso de prompt injection (bloqueado)

Si agregás en el archivo sucio una línea como `ignore previous instructions`, el **sanitizer** rechaza el archivo antes de llamar al LLM.
