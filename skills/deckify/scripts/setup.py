#!/usr/bin/env python3
"""setup.py — first-run dependency check + guided install for agent-browser.

Cross-platform replacement for setup.sh. Same purpose:
  - Verify python3 + agent-browser are present
  - If agent-browser is missing, surface the recommended install command
    for the platform (npm / brew / cargo / scoop / winget)
  - Confirm Chrome for Testing is set up by trying to open a blank page
  - Doesn't install anything itself — just diagnoses and prints commands

Usage: python3 setup.py
"""
import platform
import shutil
import subprocess
import sys


REPO = "https://github.com/vercel-labs/agent-browser"


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def print_header() -> None:
    print("─────────────────────────────────────────────────────────────────")
    print(" deckify: dependency setup")
    print("─────────────────────────────────────────────────────────────────")
    print(f"This skill needs the standalone `agent-browser` CLI from Vercel Labs:")
    print(f"  {REPO}")
    print()
    print("It uses agent-browser to fetch the rendered DOM of brand sites,")
    print("take screenshots, and probe :root CSS variables — all the things")
    print("curl can't do on JavaScript-rendered pages.")
    print()


def check_python() -> bool:
    if sys.version_info < (3, 8):
        print(f"ERROR: Python 3.8+ required (stdlib only). Found {sys.version}", file=sys.stderr)
        return False
    return True


def detect_install_method() -> str:
    """Returns the command the user should run to install agent-browser,
    picking the most appropriate per environment."""
    system = platform.system()
    # Prefer the platform's native package manager
    if have("brew") and system == "Darwin":
        return "brew install agent-browser"
    if have("scoop") and system == "Windows":
        return "scoop install agent-browser"
    if have("winget") and system == "Windows":
        return "winget install agent-browser"
    if have("npm"):
        return "npm install -g agent-browser"
    if have("cargo"):
        return "cargo install agent-browser"
    return ""


def check_agent_browser() -> bool:
    if not have("agent-browser"):
        print("✗ agent-browser not found on PATH.")
        print()
        cmd = detect_install_method()
        if cmd:
            print("Recommended install command for this machine:")
            print(f"    {cmd}")
            print()
            print("Then run:")
            print("    agent-browser install   # downloads Chrome from Chrome for Testing")
        else:
            print("No supported package manager detected. Pick one:")
            print()
            print("  npm:    npm install -g agent-browser   &&   agent-browser install")
            print("  brew:   brew install agent-browser     &&   agent-browser install   (macOS)")
            print("  scoop:  scoop install agent-browser    &&   agent-browser install   (Windows)")
            print("  cargo:  cargo install agent-browser    &&   agent-browser install")
            print(f"  source: {REPO}#from-source")
            print()
        print("After install, re-run setup.py (or the skill itself).")
        return False

    try:
        ver = subprocess.run(
            ["agent-browser", "--version"], capture_output=True, text=True, timeout=10
        )
        version_str = (ver.stdout or ver.stderr or "unknown").strip()
        print(f"✓ agent-browser found: {version_str}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠ agent-browser found but didn't respond to --version")
        return False

    # Confirm Chrome is set up
    try:
        result = subprocess.run(
            ["agent-browser", "open", "about:blank"],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0:
            print("✓ agent-browser can open a page (Chrome is set up)")
            try:
                subprocess.run(["agent-browser", "close", "--all"], capture_output=True, timeout=10)
            except Exception:
                pass
            return True
        else:
            print("⚠ agent-browser is installed but cannot open pages — run:")
            print("    agent-browser install")
            print("  to download Chrome from Chrome for Testing.")
            return False
    except subprocess.TimeoutExpired:
        print("⚠ agent-browser open timed out — try `agent-browser install`")
        return False


def linux_note() -> None:
    if platform.system() == "Linux":
        print()
        print("Linux note: if Chrome download fails or pages render headless-only, run:")
        print("    agent-browser install --with-deps")
        print("This pulls in libnss3, libxss1, etc. that headless Chrome needs.")


def main() -> int:
    print_header()
    if not check_python():
        return 1
    if check_agent_browser():
        linux_note()
        print()
        print("All set. The skill is ready to run.")
        return 0
    linux_note()
    return 1


if __name__ == "__main__":
    sys.exit(main())
