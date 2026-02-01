#!/bin/bash
# Control Minecraft Bot Bridge service

SERVICE="minecraft-bridge"

case "$1" in
    status)
        systemctl status $SERVICE --no-pager
        ;;
    logs)
        journalctl -u $SERVICE -f
        ;;
    restart)
        sudo systemctl restart $SERVICE
        echo "✅ Restarted"
        ;;
    stop)
        sudo systemctl stop $SERVICE
        echo "✅ Stopped"
        ;;
    start)
        sudo systemctl start $SERVICE
        echo "✅ Started"
        ;;
    *)
        echo "🎮 Minecraft Bot Bridge Control"
        echo "Usage: $0 {status|logs|restart|stop|start}"
        exit 1
        ;;
esac
