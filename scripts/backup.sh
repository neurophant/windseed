DATE=$(date '+%Y-%m-%d-%H-%M-%S')
DUMPNAME='backup-'$DATE$'.dump'

source .env/bin/activate
source scripts/env.sh

sudo -u postgres pg_dump ${WINDSEED_DBNAME} -f '/tmp/'$DUMPNAME
sudo mv '/tmp/'$DUMPNAME 'backups/'$DUMPNAME
