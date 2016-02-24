source .env/bin/activate
source scripts/env.sh

sudo -u postgres psql -c "DROP DATABASE ${WINDSEED_DBNAME};"
sudo -u postgres psql -c "DROP USER ${WINDSEED_USER};"
sudo -u postgres psql -c "CREATE USER ${WINDSEED_USER} WITH PASSWORD '${WINDSEED_PASSWORD}';"
sudo -u postgres psql -c "CREATE DATABASE ${WINDSEED_DBNAME} WITH OWNER=${WINDSEED_USER} ENCODING='utf-8';"

python -m windseed.utils.tables
