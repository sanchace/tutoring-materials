#!/bin/sh

# Print instructions
echo "Hello! This script installs Homebrew, Emacs, Python, and Haskell
on Mac; when prompted, enter your password (so that permission is granted to
install stuff). Nothing will appear on screen (for security reaons)
when you type it in."

# Wait for instructions to be read
read -p "Press enter to continue."

# Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/easyosx/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"

# Install Emacs
brew tap railwaycat/emacsmacport && brew install emacs-mac &

# Install Python with homebrew
brew install python &

# Install Haskell with homebrew
brew install ghcup && ghcup install ghc cabal
