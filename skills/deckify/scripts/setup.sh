#!/usr/bin/env bash
# setup.sh — first-run dependency check + guided install for agent-browser.
#
# Run this once before your first invocation of the skill, OR let fetch_site.sh
# call it automatically when it can't find the binary.
#
# Reference: https://github.com/vercel-labs/agent-browser
#
# Doesn't install ANYTHING without printing the command and asking for permission
# first — the user might prefer a different package manager.

set -euo pipefail

REPO="https://github.com/vercel-labs/agent-browser"

have() { command -v "$1" >/dev/null 2>&1; }

print_header() {
  cat <<EOF
─────────────────────────────────────────────────────────────────
 deckify: dependency setup
─────────────────────────────────────────────────────────────────
This skill needs the standalone \`agent-browser\` CLI from Vercel Labs:
  $REPO

It uses agent-browser to fetch the rendered DOM of brand sites,
take screenshots, and probe :root CSS variables — all the things
curl can't do on JavaScript-rendered pages.

EOF
}

check_python() {
  if ! have python3; then
    cat <<EOF >&2
ERROR: python3 is required (stdlib only) for the deterministic
brand-token extractor. Install Python 3.8+ from https://python.org
or via your package manager:
  macOS:  brew install python
  Linux:  apt-get install python3   |   dnf install python3
EOF
    return 1
  fi
}

detect_install_method() {
  # Returns the command the user should run to install agent-browser,
  # picking the most appropriate per environment.
  local platform; platform="$(uname -s)"

  if have brew && [[ "$platform" == "Darwin" ]]; then
    echo "brew install agent-browser"
    return
  fi
  if have npm; then
    echo "npm install -g agent-browser"
    return
  fi
  if have cargo; then
    echo "cargo install agent-browser"
    return
  fi
  # Nothing detected — surface the full matrix.
  echo ""
}

check_agent_browser() {
  if have agent-browser; then
    local ver; ver="$(agent-browser --version 2>&1 || echo unknown)"
    echo "✓ agent-browser found: $ver"
    # Confirm Chrome is set up (agent-browser install only needs to run once).
    if agent-browser open about:blank >/dev/null 2>&1; then
      echo "✓ agent-browser can open a page (Chrome is set up)"
      agent-browser close --all >/dev/null 2>&1 || true
      return 0
    else
      echo "⚠ agent-browser is installed but cannot open pages — run:"
      echo "    agent-browser install"
      echo "  to download Chrome from Chrome for Testing."
      return 1
    fi
  fi

  echo "✗ agent-browser not found on PATH."
  echo
  local cmd; cmd="$(detect_install_method)"
  if [[ -n "$cmd" ]]; then
    echo "Recommended install command for this machine:"
    echo "    $cmd"
    echo
    echo "Then run:"
    echo "    agent-browser install   # downloads Chrome from Chrome for Testing"
  else
    cat <<EOF
No supported package manager detected. Pick one:

  npm:    npm install -g agent-browser   &&   agent-browser install
  brew:   brew install agent-browser     &&   agent-browser install   (macOS)
  cargo:  cargo install agent-browser    &&   agent-browser install
  source: $REPO#from-source

EOF
  fi
  echo
  echo "After install, re-run setup.sh (or the skill itself) — it will detect the binary automatically."
  return 1
}

# Linux note about system deps
linux_note() {
  if [[ "$(uname -s)" == "Linux" ]]; then
    cat <<EOF

Linux note: if Chrome download fails or pages render headless-only,
run:
    agent-browser install --with-deps
This pulls in libnss3, libxss1, etc. that headless Chrome needs.
EOF
  fi
}

main() {
  print_header
  check_python || exit 1
  if check_agent_browser; then
    linux_note
    echo
    echo "All set. The skill is ready to run."
    exit 0
  else
    linux_note
    exit 1
  fi
}

main "$@"
