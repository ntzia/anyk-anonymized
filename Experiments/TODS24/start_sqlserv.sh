#! /bin/sh -e
#
### BEGIN INIT INFO
# Provides:          sqlserver
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Manages SQL Server instance on Linux
### END INIT INFO

DAEMON="/opt/mssql/bin/sqlservr"
daemon_OPT=""
DAEMONUSER="mssql"
daemon_NAME="sqlservr"

export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/var/opt/mssql

# Check sqlserver is present
if [ ! -x $DAEMON ]; then
        log_failure_msg "$DAEMON not present or not executable"
        exit 1
fi

# Load init functions
. /lib/lsb/init-functions


d_start () {
        log_daemon_msg "Starting system $daemon_NAME Daemon"
        start-stop-daemon --background --name $daemon_NAME --start --quiet --chuid $DAEMONUSER --exec $DAEMON --umask 007 -- $DAEMON_OPTS --oknodo
        log_end_msg $?
}

d_stop () {
        log_daemon_msg "Stopping system $daemon_NAME Daemon"
        start-stop-daemon --name $daemon_NAME --stop --retry 5 --quiet --name $daemon_NAME --oknodo
        log_end_msg $?
}

case "$1" in

        start|stop)
                d_${1}
                ;;

        restart|reload|force-reload)
                        d_stop
                        d_start
                ;;

        force-stop)
               d_stop
                ;;

        status)
                status_of_proc "$daemon_NAME" "$DAEMON" "system-wide $daemon_NAME" && exit 0 || exit $?
                ;;
        *)
                echo "Usage: /etc/init.d/$daemon_NAME {start|stop|force-stop|restart|reload|force-reload|status}"
                exit 1
                ;;
esac
exit 0