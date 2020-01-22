import threading

# From O'Reilly Python Cookbook by David Ascher, Alex Martelli
# With changes to cover the starvation situation where a continuous
#   stream of readers may starve a writer, Lock Promotion and Context Managers
class ReadWriteLock:
    """
    A lock object that allows many simultaneous "read locks", but
    only one "write lock."
    """

    def __init__(self, withPromotion=False):
        self._read_ready = threading.Condition(threading.RLock(  ))
        self._readers = 0
        self._writers = 0
        self._promote = withPromotion
        self._readerList = []  # List of Reader thread IDs
        self._writerList = []  # List of Writer thread IDs

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire()
        try:
            while self._writers > 0:
                self._read_ready.wait()
                self._readers += 1
        finally:
            self._readerList.append(threading.get_ident())
            self._read_ready.release()

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._readerList.remove(threading.get_ident())
            self._read_ready.release()

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire()
        self._writers += 1
        self._writerList.append(threading.get_ident())
        while self._readers > 0:
            if self._promote and threading.get_ident() in self._readerList and set(self._readerList).issubset(set(self._writerList)):
                break
            else:
                self._read_ready.wait()

    def release_write(self):
        """ Release a write lock. """
        self._writers -= 1
        self._writerList.remove(threading.get_ident())
        self._read_ready.notifyAll()
        self._read_ready.release()




id_to_queue = {}
lock = ReadWriteLock()

thread_list = []
queue_list = []


def get_threads_for_ids(q_id_list):
    ret = []
    lock.acquire_read()
    for id in q_id_list:
        res = id_to_queue[id]
        if res not in ret:
            ret.append(res)
    lock.release_read()
    return ret

def set_thread_with_id(q_id, thread, queue):
    lock.acquire_write()
    id_to_queue[q_id] = queue
    queue_list.append(queue)
    thread_list.append(thread)
    lock.release_write()

def change_ids_queue(q_id, queue):
    lock.acquire_write()
    id_to_queue[q_id] = queue
    lock.release_write()

def send_all_threads(msg):
    lock.acquire_write()
    for p in queue_list:
        p.put(msg)
    lock.release_write()

def stop_all_threads():
    lock.acquire_write()
    for p in thread_list:
        p.join()
    lock.release_write()
