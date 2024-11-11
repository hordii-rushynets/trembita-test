service atd start

echo "cd /app && DIIA_API_URL=${DIIA_API_URL} POSTGRES_DB=${POSTGRES_DB} POSTGRES_USER=${POSTGRES_USER} POSTGRES_PASSWORD=${POSTGRES_PASSWORD} python3 main.py >> /var/log/trembita.log 2>&1" | at now

# echo "*/5 * * * * cd /app && DIIA_API_URL=${DIIA_API_URL} POSTGRES_DB=${POSTGRES_DB} POSTGRES_USER=${POSTGRES_USER} POSTGRES_PASSWORD=${POSTGRES_PASSWORD} python3 main.py >> /var/log/trembita.log 2>&1" > /etc/cron.d/trembita

echo "59 23 31 3,12 * cd /app && DIIA_API_URL=${DIIA_API_URL} POSTGRES_DB=${POSTGRES_DB} POSTGRES_USER=${POSTGRES_USER} POSTGRES_PASSWORD=${POSTGRES_PASSWORD} python3 main.py >> /var/log/trembita.log 2>&1" > /etc/cron.d/trembita
echo "59 23 30 6,9 * cd /app && DIIA_API_URL=${DIIA_API_URL} POSTGRES_DB=${POSTGRES_DB} POSTGRES_USER=${POSTGRES_USER} POSTGRES_PASSWORD=${POSTGRES_PASSWORD} python3 main.py >> /var/log/trembita.log 2>&1" > /etc/cron.d/trembita

chmod 0644 /etc/cron.d/trembita
crontab /etc/cron.d/trembita

touch /var/log/trembita.log

cron -f >> /var/log/trembita.log 2>&1
