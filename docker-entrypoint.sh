#!/bin/sh
# Контейнер іске қосылғанда: дерекқорды күту → миграциялар → негізгі процесс (CMD).
set -e

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    # Дерекқор контейнерден кейін іске қосылуы мүмкін — 30 секундқа дейін қайталаймыз
    attempt=1
    until alembic upgrade head; do
        if [ "$attempt" -ge 10 ]; then
            echo "Миграциялар орындалмады: дерекқор қолжетімсіз" >&2
            exit 1
        fi
        echo "Дерекқор әлі дайын емес, қайталау ($attempt/10)..." >&2
        attempt=$((attempt + 1))
        sleep 3
    done
fi

exec "$@"
