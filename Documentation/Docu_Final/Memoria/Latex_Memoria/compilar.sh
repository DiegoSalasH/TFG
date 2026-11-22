#!/usr/bin/env bash
# Compila la memoria del TFG.
#
# Uso (desde cualquier carpeta, con Git Bash en Windows o con bash en Linux):
#   ./compilar.sh            -> genera el PDF
#   ./compilar.sh --docx     -> genera el PDF y además un .docx con Pandoc
#
# Salida (en Documentation/Docu_Final/Memoria/):
#   Memoria_TFG_Diego_Salas.pdf
#   Memoria_TFG_Diego_Salas_desde_latex.docx   (solo con --docx)
#
# Los ficheros auxiliares se generan en un directorio temporal, así que la
# carpeta del LaTeX queda limpia.

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SALIDA="$(cd "$DIR/.." && pwd)"
NOMBRE="Memoria_TFG_Diego_Salas"

# --- Localizar Tectonic y Pandoc (PATH o instalación de usuario en Windows) ---
buscar() {
  local nombre="$1" alternativa="$2"
  if command -v "$nombre" >/dev/null 2>&1; then
    command -v "$nombre"
  elif [ -n "$alternativa" ] && [ -x "$alternativa" ]; then
    echo "$alternativa"
  else
    echo ""
  fi
}

LOCALAPPDATA_UNIX=""
if [ -n "${LOCALAPPDATA:-}" ]; then
  LOCALAPPDATA_UNIX="$(cygpath -u "$LOCALAPPDATA" 2>/dev/null || echo "$LOCALAPPDATA")"
fi
TECTONIC="$(buscar tectonic "$LOCALAPPDATA_UNIX/Programs/Tectonic/tectonic.exe")"
PANDOC="$(buscar pandoc "$LOCALAPPDATA_UNIX/Pandoc/pandoc.exe")"

if [ -z "$TECTONIC" ]; then
  echo "ERROR: no se encuentra Tectonic. Instálalo (https://tectonic-typesetting.github.io)." >&2
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Compilando el PDF con $(basename "$TECTONIC")..."
( cd "$DIR" && "$TECTONIC" --keep-logs --outdir "$TMP" main.tex )
cp "$TMP/main.pdf" "$SALIDA/$NOMBRE.pdf"
echo "PDF: $SALIDA/$NOMBRE.pdf"

# Avisos útiles del log
if grep -q "There were undefined references" "$TMP/main.log"; then
  echo "AVISO: hay referencias sin resolver (revisa \\ref y \\cite)." >&2
fi

if [ "${1:-}" = "--docx" ]; then
  if [ -z "$PANDOC" ]; then
    echo "ERROR: no se encuentra Pandoc; no se genera el .docx." >&2
    exit 1
  fi
  ( cd "$DIR" && "$PANDOC" main.tex --resource-path=. -o "$SALIDA/${NOMBRE}_desde_latex.docx" )
  echo "DOCX: $SALIDA/${NOMBRE}_desde_latex.docx"
fi
