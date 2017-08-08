import collectd_bucky
import signal
import multiprocessing
import Queue as queue
import cfg as cfg

class Receiver(object):
    def __init__(self):
        self.qOfSamples = multiprocessing.Queue()
        self.server = collectd_bucky.getCollectDServer(self.qOfSamples,cfg)

    def run(self):
        def sigterm_handler(signum, frame):
            self.qOfSamples.put(None)

        self.server.start()
        signal.signal(signal.SIGTERM, sigterm_handler)
        while True:
            print (self.server.queue.qsize())
            try:
                sample = self.qOfSamples.get(True, 1)
                if not sample:
                    break
                print sample
            except queue.Empty:
                print "EMpty Queue"
                pass
            except IOError:
                continue
            except KeyboardInterrupt:
                break

def main():
    receiver = Receiver()
    receiver.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
