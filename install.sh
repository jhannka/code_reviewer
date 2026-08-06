#!/usr/bin/env bash
# Resolve absolute path of current folder
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Target path for global symlink
TARGET_SYM="/usr/local/bin/code-reviewer"

echo "Installing code-reviewer command globally..."
echo "Creating symlink: $PROJECT_DIR/bin/code-reviewer -> $TARGET_SYM"

# Check if target exists and delete if it's a symlink
if [ -L "$TARGET_SYM" ] || [ -f "$TARGET_SYM" ]; then
    echo "Target symlink already exists. Removing it first..."
    sudo rm -f "$TARGET_SYM"
fi

# Ensure executable permissions
chmod +x "$PROJECT_DIR/bin/code-reviewer"

# Create symbolic link requiring root access
if sudo ln -s "$PROJECT_DIR/bin/code-reviewer" "$TARGET_SYM"; then
    echo "✅ Success! 'code-reviewer' is now installed globally."
    echo "You can run it from any project directory using: code-reviewer"
else
    echo "❌ Error: Failed to create symlink at $TARGET_SYM."
fi
