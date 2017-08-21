import collectd_bucky
import signal
import multiprocessing
import Queue as queue
import cfg as cfg
import collections
import collectd_analytics as ca


interrupted = False

def sigint_handler(signal):
    global interrupted
    interrupted = True

class Receiver(object):
    def __init__(self):
        self.qOfSamples = multiprocessing.Queue()
        self.server = collectd_bucky.getCollectDServer(self.qOfSamples,cfg)
        self.pdDict = collections.defaultdict(list)

    def run(self):
        def sigterm_handler(signum, frame):
            self.qOfSamples.put(None)

        self.server.start()
        signal.signal(signal.SIGTERM, sigterm_handler)
        #signal.signal(signal.SIGINT, sigterm_handler)
        while True:
            try:
                sample = self.qOfSamples.get(True, 1)
                if not sample:
                    break
                self.handle(sample)
            except queue.Empty:
                pass
            except IOError:
                continue
            except KeyboardInterrupt:
                break
            if interrupted:
                break
        ca.plotGraphs(self.pdDict)

    def handle(self, sample):
        ''' Store the following:
            1. cpu-idle, cpu-system and cpu-user metrics
            2. processes cpu-system, cpu-idle and rss
            3. Dropped packets of interfaces except loopback
            '''
        if (('cpu' in sample[1] and
            any(s in sample[1] for s in ('idle', 'user','system'))) or
            ('processes' in sample[1] and 'ovs' in sample[1] and
             any(p in sample[1] for p in ('user', 'system', 'rss'))) or
            ('dropped' in sample[1] and 'lo' not in sample[1])):
            self.pdDict[sample[1]].append((sample[2], sample[3]))
            if len(self.pdDict[sample[1]]) > 50:
                interrupted = True
        #print self.pdDict

    def stop(self):
        pass

    def analysze(self):
        pass

def main():
    receiver = Receiver()
    receiver.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
