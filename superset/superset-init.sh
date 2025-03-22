#!/bin/bash


# create Admin user, you can read these values from env or anywhere else possible
superset fab create-adin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "&ADMIN_EMAIL"

# upgrading superset metastore
superset db upgrade

# setup roles and permissions
superset superset init

# starting server
/bin/sh -c /user/bin/run-server.sh