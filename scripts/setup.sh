#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${TOOLS_DIR:-$ROOT_DIR/.tools}"
CODEQL_VERSION="${CODEQL_VERSION:-2.25.5}"
CODEQL_SHA256="${CODEQL_SHA256:-76cd9d785940da0a5876676136be0c2803baa116304af5265052b74f1ec46258}"
ARCHIVE="codeql-bundle-linux64.tar.zst"
DOWNLOAD_URL="https://github.com/github/codeql-action/releases/download/codeql-bundle-v${CODEQL_VERSION}/${ARCHIVE}"
INSTALL_DIR="$TOOLS_DIR/codeql-$CODEQL_VERSION"
ARCHIVE_PATH="$TOOLS_DIR/$ARCHIVE"
AMD64_ROOTFS="$TOOLS_DIR/amd64-rootfs"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: no se encontró '$1' en PATH" >&2
    exit 1
  fi
}

require_command uv
require_command curl
require_command sha256sum
require_command tar

case "$(uname -m)" in
  x86_64|amd64) ;;
  aarch64|arm64)
    require_command docker
    if ! grep -qs '^enabled' /proc/sys/fs/binfmt_misc/qemu-x86_64 2>/dev/null; then
      cat >&2 <<'EOF'
error: CodeQL sólo publica el bundle Linux para x86_64 y este host es ARM64.
Activa la emulación una vez por arranque con:
  docker run --privileged --rm tonistiigi/binfmt --install amd64
EOF
      exit 1
    fi
    if [[ ! -e "$AMD64_ROOTFS/lib64/ld-linux-x86-64.so.2" ]]; then
      echo "Preparando un userland amd64 local para CodeQL..."
      container="$(docker create --platform linux/amd64 ubuntu:24.04)"
      trap 'docker rm -f "$container" >/dev/null 2>&1 || true' EXIT
      mkdir -p "$AMD64_ROOTFS"
      docker export "$container" | tar -xf - -C "$AMD64_ROOTFS"
      docker rm "$container" >/dev/null
      trap - EXIT
    fi
    ;;
  *)
    echo "error: arquitectura no soportada por este setup: $(uname -m)" >&2
    exit 1
    ;;
esac

cd "$ROOT_DIR"
echo "Preparando el entorno Python..."
uv sync --frozen

mkdir -p "$TOOLS_DIR"
if [[ ! -x "$INSTALL_DIR/codeql/codeql" ]]; then
  echo "Descargando CodeQL $CODEQL_VERSION..."
  curl --fail --location --retry 3 --output "$ARCHIVE_PATH" "$DOWNLOAD_URL"
  echo "$CODEQL_SHA256  $ARCHIVE_PATH" | sha256sum --check --status || {
    echo "error: el checksum del bundle de CodeQL no coincide" >&2
    exit 1
  }
  staging="$TOOLS_DIR/.codeql-$CODEQL_VERSION.tmp"
  rm -rf "$staging"
  mkdir -p "$staging"
  tar --zstd -xf "$ARCHIVE_PATH" -C "$staging"
  mv "$staging" "$INSTALL_DIR"
  rm -f "$ARCHIVE_PATH"
fi

ln -sfn "codeql-$CODEQL_VERSION" "$TOOLS_DIR/codeql-current"

echo "Validando la instalación..."
"$ROOT_DIR/scripts/codeql" version
"$ROOT_DIR/scripts/codeql" resolve languages | grep -E '^python' >/dev/null
uv run python -m pytest -q

cat <<EOF

Setup completado.
  Python:  $ROOT_DIR/.venv/bin/python
  CodeQL:  $ROOT_DIR/scripts/codeql

El launcher ./run_experiment.sh detecta automáticamente este CodeQL local.
EOF
