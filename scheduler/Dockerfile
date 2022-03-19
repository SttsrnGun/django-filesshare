FROM alpine:latest

# Install prerequisites
RUN apk add --no-cache curl

COPY scheduler/cron /etc/crontabs/root
# COPY cron /etc/crontabs/root

CMD ["/usr/sbin/crond", "-f"]