#!/usr/bin/env bash
# Install OmniRoute and connect it to Claude Code (macOS / Linux).
# Usage: bash setup-omniroute.sh
set -e

command -v node >/dev/null || { echo "Node.js is required (v20+): https://nodejs.org"; exit 1; }

echo "==> Installing OmniRoute..."
npm install -g --allow-scripts=omniroute,keytar,onnxruntime-node,@parcel/watcher,@swc/core,protobufjs,esbuild omniroute \
  || npm install -g omniroute

if ! command -v claude >/dev/null; then
  echo "==> Installing Claude Code..."
  npm install -g @anthropic-ai/claude-code
fi

echo "==> Starting OmniRoute in the background (log: ~/omniroute.log)..."
nohup omniroute > ~/omniroute.log 2>&1 &
sleep 8

echo
echo "Open http://localhost:20128 in your browser:"
echo "  1) Providers -> add a provider and its API key"
echo "  2) Endpoints -> copy your OmniRoute key"
echo
read -rp "Paste your OmniRoute key here: " OMNI_KEY
[ -z "$OMNI_KEY" ] && { echo "No key entered. Run again once you have it."; exit 1; }

RC="$HOME/.bashrc"; [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ] && RC="$HOME/.zshrc"
{
  echo ""
  echo "# OmniRoute -> Claude Code"
  echo "export ANTHROPIC_BASE_URL=http://localhost:20128"
  echo "export ANTHROPIC_AUTH_TOKEN=$OMNI_KEY"
} >> "$RC"

echo
echo "Done. Saved settings to $RC"
echo "Open a new terminal and run: claude"
echo "(Or skip the env vars and run: omniroute launch)"
