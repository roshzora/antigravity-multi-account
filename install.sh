#!/usr/bin/env bash
#
# Antigravity Multi-Account Manager (agm) Installer
#
set -e

BOLD="\033[1m"
GREEN="\033[92m"
CYAN="\033[96m"
YELLOW="\033[93m"
RESET="\033[0m"

echo -e "${CYAN}${BOLD}Installing Antigravity Multi-Account Manager (agm)...${RESET}\n"

# Verify Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "${YELLOW}Error: Python 3 is required but not installed.${RESET}"
    exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
SHARE_DIR="$HOME/.local/share/agy-accounts"

mkdir -p "$BIN_DIR"
mkdir -p "$HOME/.local/share"

# Link or update share directory
rm -rf "$SHARE_DIR"
ln -sf "$PROJECT_DIR" "$SHARE_DIR"

# Install binary entrypoints
cat << 'EOF' > "$BIN_DIR/agm"
#!/usr/bin/env python3
import sys
from pathlib import Path

pkg_dir = Path(__file__).resolve().parent.parent / "share" / "agy-accounts"
if str(pkg_dir) not in sys.path:
    sys.path.insert(0, str(pkg_dir))

from agm.cli import main

if __name__ == "__main__":
    main()
EOF

chmod +x "$BIN_DIR/agm"
ln -sf "$BIN_DIR/agm" "$BIN_DIR/agy-multi"

echo -e "✔ Binaries installed to ${BOLD}$BIN_DIR/agm${RESET} and ${BOLD}$BIN_DIR/agy-multi${RESET}"

# Configure shell integration in ~/.bashrc if not present
if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "agm run" "$HOME/.bashrc"; then
        echo -e "\n# Antigravity Multi-Account Integration" >> "$HOME/.bashrc"
        echo -e "agy() {" >> "$HOME/.bashrc"
        echo -e "    if [[ \"\$1\" == @* ]]; then" >> "$HOME/.bashrc"
        echo -e "        local profile=\"\${1#@}\"" >> "$HOME/.bashrc"
        echo -e "        shift" >> "$HOME/.bashrc"
        echo -e "        agm run \"\$profile\" \"\$@\"" >> "$HOME/.bashrc"
        echo -e "    else" >> "$HOME/.bashrc"
        echo -e "        command agy \"\$@\"" >> "$HOME/.bashrc"
        echo -e "    fi" >> "$HOME/.bashrc"
        echo -e "}" >> "$HOME/.bashrc"
        echo -e "✔ Configured shell dispatcher in ${BOLD}~/.bashrc${RESET}"
    else
        echo -e "✔ Shell integration already configured in ${BOLD}~/.bashrc${RESET}"
    fi
fi

# Run diagnostics
echo -e "\n${CYAN}Running system diagnostics...${RESET}"
"$BIN_DIR/agm" doctor

echo -e "${GREEN}${BOLD}Installation complete!${RESET}"
echo -e "Try: ${CYAN}agm list${RESET} or ${CYAN}agm add <profile_name>${RESET}\n"
