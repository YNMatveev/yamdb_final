#!/bin/sh

# Decrypt the file
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$GPG_SECRET_PASSPHRASE" \
--output $GITHUB_WORKSPACE/.env .env.gpg