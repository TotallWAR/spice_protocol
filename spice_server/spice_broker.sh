#!/bin/sh
# chkconfig: 123456 90 10
# TTS Server for Speech Synthesis
#
workdir=/etc/speech
 
start() {
    cd $workdir
    /usr/bin/python /spice_server/spice_broker.py &
    echo "Server started."
}
	     
stop() {
    pid=`ps -ef | grep '[p]ython /etc/speech/TTSserver.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}
				 
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage: /etc/init.d/tornado-tts {start|stop|restart}"
        exit 1
esac
exit 0

