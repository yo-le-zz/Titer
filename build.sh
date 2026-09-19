#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/.build"
NUITKA_OUTPUT="$BUILD_DIR/nuitka"

PACKAGE_NAME="titer"

VERSION="$(
    python3 -c '
import tomllib

with open("pyproject.toml", "rb") as file:
    print(tomllib.load(file)["project"]["version"])
'
)"

ARCH="x86_64"

PACKAGE_DIR="$BUILD_DIR/${PACKAGE_NAME}_v${VERSION}_${ARCH}"
OUTPUT="$DIST_DIR/${PACKAGE_NAME}_v${VERSION}_${ARCH}.deb"

echo "==> Building $PACKAGE_NAME v$VERSION"

echo "==> Cleaning previous builds"

rm -rf "$DIST_DIR"
rm -rf "$BUILD_DIR"

mkdir -p "$DIST_DIR"
mkdir -p "$NUITKA_OUTPUT"
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/usr/lib/titer"
mkdir -p "$PACKAGE_DIR/usr/bin"

echo "==> Checking dependencies"

for command in python3 uv dpkg-deb; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "Error: $command is not installed."
        exit 1
    fi
done

echo "==> Installing build dependencies"

uv sync

echo "==> Checking Nuitka"

if ! uv run python -c "import nuitka" >/dev/null 2>&1; then
    echo "==> Installing Nuitka"
    uv add --dev nuitka
fi

echo "==> Compiling with Nuitka"

uv run nuitka \
    --standalone \
    --output-dir="$NUITKA_OUTPUT" \
    --output-filename=titer \
    "$PROJECT_DIR/src/titer/__main__.py"

NUITKA_DIST="$NUITKA_OUTPUT/__main__.dist"

if [ ! -f "$NUITKA_DIST/titer" ]; then
    echo "Error: Nuitka executable was not found."
    exit 1
fi

echo "==> Preparing Debian package"

cp -a \
    "$NUITKA_DIST/." \
    "$PACKAGE_DIR/usr/lib/titer/"

chmod 755 "$PACKAGE_DIR/usr/lib/titer/titer"

echo "==> Creating Debian launcher"

cat > "$PACKAGE_DIR/usr/bin/titer" <<'EOF'
#!/usr/bin/env bash

exec /usr/lib/titer/titer "$@"
EOF

chmod 755 "$PACKAGE_DIR/usr/bin/titer"

echo "==> Creating Debian metadata"

cat > "$PACKAGE_DIR/DEBIAN/control" <<EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: devel
Priority: optional
Architecture: amd64
Maintainer: yolezz
Description: Interactive CLI project generator
 Titer is a CLI tool for initializing projects
 with interactive questions and configurations.
 .
 Titer provides interactive project generation
 for Python and other languages in future releases.
EOF

echo "==> Building Debian package"

dpkg-deb --build \
    "$PACKAGE_DIR" \
    "$OUTPUT"

echo
echo "✓ Build complete"
echo
echo "Package:"
echo "  $OUTPUT"
echo
echo "Install with:"
echo "  sudo apt install ./$OUTPUT"
echo
echo "Test with:"
echo "  titer --help"