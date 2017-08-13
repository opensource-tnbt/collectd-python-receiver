import collectd_bucky
import signal
import multiprocessing
import Queue as queue
import cfg as cfg
import collections


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
        while True:
            print (self.server.queue.qsize())
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

    def handle(self, sample):
        if 'dropped' in sample[1] and 'lo' not in sample[1]:
            self.pdDict[sample[1]].append((sample[2], sample[3]))
        print self.pdDict

def main():
    receiver = Receiver()
    receiver.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
