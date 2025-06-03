#!/bin/bash
# Interpreter identifier

set -e
# Exit on fail

pnpm install
# Ensure all node modules are installed.

pnpm build
# Ensure the project is built

# Start the server
pnpm preview --host

exec "$@"
# Finally call command issued to the docker service