#! /bin/sh
case "$1" in
    start)
        echo "nameserver 8.8.8.8" > /etc/resolv.conf
        python3 /home/root/main.py &
        ;;
    *)
        ;;
esac
exit 0