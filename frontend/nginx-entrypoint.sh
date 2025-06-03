#!/bin/sh
set -e

ASSETS_DIR="/usr/share/nginx/html"

VITE_VARIABLES="
VITE_API_URL
VITE_OLLAMA_BASE_URL
"
# Add any other VITE_ variables your app uses to the list above.

find "$ASSETS_DIR" -type f \( -name '*.js' -o -name '*.html' -o -name '*.css' \) -print0 | while IFS= read -r -d $'\0' file; do
  for var_name in $VITE_VARIABLES; do
    placeholder="__${var_name}__"
    var_value=$(printenv "$var_name")

    if [ -n "$var_value" ]; then
      escaped_value=$(echo "$var_value" | sed -e 's/\\/\\\\/g' -e 's/\//\\\//g' -e 's/&/\\\&/g')
      if grep -q "$placeholder" "$file"; then
        sed -i "s/${placeholder}/${escaped_value}/g" "$file"
      fi
    fi
  done
done

exec "$@"