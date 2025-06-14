#!/bin/sh

# Required - uv installation
if command -v uv >/dev/null 2>&1; then
  echo "✅ uv is installed"
else
  echo "❌ uv is not installed. Installing now..."
  curl -Ls https://astral.sh/uv/install.sh | sh
fi


# setup virtual environment
uv venv
