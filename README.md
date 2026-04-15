# The Clean Code Bot (Automated Refactorer)

CLI en **Python** que toma un archivo de código “sucio” o poco documentado y produce una versión **refactorizada** alineada con **SOLID**, con **documentación técnica** (docstrings estilo Google o NumPy según el modelo).

Incluye:

- **Plantillas de prompt** con **Chain of Thought (CoT)**: el modelo primero analiza el código y luego propone mejoras.
- **Validación y saneamiento** de entrada para mitigar **Prompt Injection** (patrones bloqueados, límites de tamaño, delimitadores seguros).
- Soporte **Groq** (tier gratuito, API compatible OpenAI) u **OpenAI** (pay-as-you-go).

## Requisitos

- Python 3.10+
- Clave API: [Groq](https://console.groq.com/keys) y/o [OpenAI](https://platform.openai.com/api-keys)

## Instalación: entorno virtual (`venv`)

Conviene usar un **entorno virtual** (carpeta local, p. ej. `.venv`) para aislar las dependencias del proyecto del Python global. Eso **no** es lo mismo que el archivo **`.env`** (variables de API): el venv es el intérprete y los paquetes; el `.env` son claves y opciones del LLM.

Trabajá siempre desde la carpeta del proyecto **`clean-code-bot/`** (donde está `requirements.txt`).

### 1. Comprobar Python

Necesitás **Python 3.10 o superior** instalado y accesible como `python` o `python3`:

```bash
python --version
# o, en muchas distribuciones Linux:
python3 --version
```

Si solo tenés `python3`, usá `python3` en lugar de `python` en los comandos siguientes.

### 2. Crear el entorno virtual

```bash
cd clean-code-bot
python -m venv .venv
```

Eso crea la carpeta **`.venv/`** (ya está en `.gitignore`; no la subas al repositorio). El nombre `.venv` es convención; podés usar otro (p. ej. `venv`), pero estos ejemplos asumen **`.venv`**.

### 3. Activar el entorno virtual

Hasta que no actives el venv, `pip` y `python` pueden apuntar al sistema. Después de activar, el prompt suele mostrar `(.venv)`.

**Windows — PowerShell:**

```powershell
Set-Location ruta\a\clean-code-bot
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea scripts, ejecutá una vez (como administrador o en tu usuario):  
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Windows — CMD:**

```cmd
cd ruta\a\clean-code-bot
.venv\Scripts\activate.bat
```

**Linux o macOS (bash/zsh):**

```bash
cd ruta/a/clean-code-bot
source .venv/bin/activate
```

### 4. Instalar dependencias del proyecto

Con el venv **activado**:

```bash
pip install -r requirements.txt
```

Opcional: comprobá que usás el pip del venv:

```bash
python -m pip --version
```

La ruta debería incluir `.venv`.

### 5. Desactivar el entorno virtual

Cuando termines de trabajar en el proyecto:

```bash
deactivate
```

No borra la carpeta `.venv`; solo deja de usarla en esa terminal. La próxima vez, volvé a ejecutar el paso **Activar**.

## Configuración del archivo `.env`

El bot lee variables de entorno con **`python-dotenv`**: busca un archivo **`.env`** en el directorio desde el cual ejecutás el comando (normalmente la raíz del proyecto `clean-code-bot/`). Sin clave API válida, el comando `refactor` fallará al llamar al modelo.

### 1. Crear `.env` a partir del ejemplo

En la carpeta `clean-code-bot` (donde está `.env.example`):

**Windows (PowerShell o CMD):**

```powershell
copy .env.example .env
```

**Linux o macOS:**

```bash
cp .env.example .env
```

Eso crea **`.env`** con plantillas vacías. El archivo **`.env`** ya está listado en `.gitignore`: no lo subas al repositorio.

### 2. Obtener una clave API

- **Groq (recomendado para probar):** cuenta gratuita y clave en [console.groq.com/keys](https://console.groq.com/keys).
- **OpenAI:** clave en [platform.openai.com/api-keys](https://platform.openai.com/api-keys) (requiere crédito según tu cuenta).

### 3. Editar `.env` con un editor de texto

Abrí `.env` en VS Code, Cursor, Notepad, etc., y completá al menos **una** de estas líneas (sin comillas salvo que la clave las incluya literalmente):

| Variable | Uso |
|----------|-----|
| `GROQ_API_KEY` | Obligatoria si usás Groq. Ejemplo: `GROQ_API_KEY=gsk_...` |
| `OPENAI_API_KEY` | Obligatoria si usás OpenAI. Ejemplo: `OPENAI_API_KEY=sk-...` |
| `LLM_PROVIDER` | `groq` u `openai`. Si lo omitís, el programa elige por defecto según qué clave exista (`groq` si hay `GROQ_API_KEY`). |
| `LLM_MODEL` | Modelo concreto; si está vacío, se usa un valor por defecto según el proveedor (ver `.env.example`). |

**Buenas prácticas:**

- Una variable por línea; sin espacios alrededor del `=` (evitá `KEY = valor`).
- No pegues la clave en el chat ni en issues de GitHub.
- Si cambiás `.env`, guardá el archivo y volvé a ejecutar el CLI desde la misma carpeta donde está `.env`, o exportá las variables en la terminal si preferís no usar archivo.

### 4. Comprobar que se carga

Con el entorno virtual activado y estando en `clean-code-bot/`:

```bash
python -m clean_code_bot refactor examples/dirty_calculator.py --dry-run
```

Si la clave y el proveedor son correctos, deberías ver la respuesta larga del modelo (análisis CoT + código). Sin `.env` o con clave inválida, verás un error claro en consola.

## Uso

Activá antes el **venv** (apartado *Instalación: entorno virtual* más arriba) y ubicáte en `clean-code-bot/`:

```bash
python -m clean_code_bot refactor path/al/archivo_sucio.py -o salida.py
```

Opciones útiles:

| Opción | Descripción |
|--------|-------------|
| `-o`, `--output` | Archivo de salida (si no se indica, imprime en stdout) |
| `--provider` | `groq` o `openai` (sobreescribe env) |
| `--model` | Modelo concreto (sobreescribe env) |
| `--dry-run` | Imprime la respuesta completa del modelo (CoT + código) sin extraer solo el bloque cercado |

Ejemplo:

```bash
python -m clean_code_bot refactor examples/dirty_calculator.py -o examples/clean_calculator_generated.py
```

## Entrega del curso (checklist)

- [x] Repositorio con el paquete fuente (`clean_code_bot/`)
- [x] `requirements.txt`
- [x] Carpeta `examples/` con muestras antes / después

## Seguridad (Prompt Injection)

El código de usuario **no** se concatena como instrucciones del sistema: va dentro de bloques delimitados y se filtran frases típicas de inyección. Ver `clean_code_bot/sanitizer.py` y la documentación en comentarios. **No sustituye** revisión humana ni auditoría de seguridad.

## Licencia

MIT
