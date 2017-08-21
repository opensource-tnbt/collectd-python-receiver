import os
import sys
import signal
import time
import subprocess

DIRS = ['/var/run/', '/opt/collectd/var/run/']
FILENAME = 'collectd.pid'
EXECNAME = 'collectd'
EXECPATH = '/opt/collectd/sbin/'

def CheckProcess():
        """Checks if daemon is started
        args - process start arguments
        pidfile - file with stored process pid
        If daemon is running returns process ID
        If daemon is not started returns False
        If pidFile is not exist returns None"""
        for dir in DIRS:
            if os.path.exists(os.path.join(dir, FILENAME)):
                try:
                    with open(os.path.join(dir,FILENAME)) as pidReader:
                        pid = int(pidReader.readline())
                except (ValueError, IOError), e:
                    return None
                try:
                    cmdfile = "/proc/%s/cmdline" % pid
                    if not os.path.isfile(cmdfile):
                        return False
                    with open(cmdfile) as psReader:
                        psLine = psReader.read()
                        if EXECNAME in psLine:
                            return pid
                    return False
                except:
                    print("error while reading process status")

def StopProcess():
    stTime = time.time()
    pid = CheckProcess()
    if pid > 0:
        pgid = os.getpgid(pid)
        os.killpg(pgid, signal.SIGTERM)
        time.sleep(0.1)
        while os.path.isdir("/proc/%s" % pid) and (
            time.time() - stTime < timeout):
            time.sleep(0.01)
        if os.path.isdir("/proc/%s" % pid):
            os.killpg(pgid, signal.SIGKILL)
        result = not os.path.isdir("/proc/%s" % pid)
        return result
    else:
        raise RuntimeError("can't determine daemon pid")

def StartProcess():
    proc = subprocess.Popen(['./'+EXECNAME], stdin=None, stdout=None,
                           stderr=None, cwd=EXECPATH)
    return proc.pid()

if __name__ == "__main__":
    check = CheckProcess()
    if check == None or check == False:
        print("Collectd not yet started .. Starting now...")
        proc = StartProcess()
    else:
        print("The PID is", check)
        if StopProcess():
            print("Successfully Stopped..")
