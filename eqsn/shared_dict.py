import threading


class SharedDict(object):

    # From O'Reilly Python Cookbook by David Ascher, Alex Martelli
    # With changes to cover the starvation situation where a continuous
    #   stream of readers may starve a writer, Lock Promotion and Context Managers
    class ReadWriteLock:
        """
        A lock object that allows many simultaneous "read locks", but
        only one "write lock."
        """

        def __init__(self, with_promotion=False):
            self._read_ready = threading.Condition(threading.RLock())
            self._readers = 0
            self._writers = 0
            self._promote = with_promotion
            self._readerList = []  # List of Reader thread IDs
            self._writerList = []  # List of Writer thread IDs

        def acquire_read(self):
            """
            Acquire a read lock. Blocks only if a thread has
            acquired the write lock.
            """
            self._read_ready.acquire()
            try:
                while self._writers > 0:
                    self._read_ready.wait()
                    self._readers += 1
            finally:
                self._readerList.append(threading.get_ident())
                self._read_ready.release()

        def release_read(self):
            """
            Release a read lock.
            """
            self._read_ready.acquire()
            try:
                self._readers -= 1
                if not self._readers:
                    self._read_ready.notifyAll()
            finally:
                self._readerList.remove(threading.get_ident())
                self._read_ready.release()

        def acquire_write(self):
            """
            Acquire a write lock. Blocks until there are no
            acquired read or write locks.
            """
            self._read_ready.acquire()
            self._writers += 1
            self._writerList.append(threading.get_ident())
            while self._readers > 0:
                if self._promote and threading.get_ident() in self._readerList and set(self._readerList).issubset(
                        set(self._writerList)):
                    break
                else:
                    self._read_ready.wait()

        def release_write(self):
            """
            Release a write lock.
            """
            self._writers -= 1
            self._writerList.remove(threading.get_ident())
            self._read_ready.notifyAll()
            self._read_ready.release()

    __instance = None

    @staticmethod
    def get_instance():
        if SharedDict.__instance is None:
            return SharedDict()
        return SharedDict.__instance

    @staticmethod
    def get_new_instance():
        SharedDict.__instance = None
        return SharedDict()

    def __init__(self):
        if SharedDict.__instance is not None:
            raise Exception("Call get instance to get this class!")
        SharedDict.__instance = self
        self.lock = SharedDict.ReadWriteLock()
        self.id_to_queue = {}

        self.id_to_thread = {}
        self.thread_list = []
        self.queue_list = []

    def block_shared_dict(self):
        self.lock.acquire_write()

    def release_shared_dict(self):
        self.lock.release_write()

    def get_queues_and_threads_for_ids(self, q_id_list):
        ret = []
        self.lock.acquire_read()
        for q_id in q_id_list:
            res = self.id_to_queue[q_id]
            res2 = self.id_to_thread[q_id]
            if res not in ret:
                ret.append((res, res2))
        self.lock.release_read()
        return ret

    def get_queues_for_ids(self, q_id_list):
        ret = []
        self.lock.acquire_read()
        for q_id in q_id_list:
            res = self.id_to_queue[q_id]
            if res not in ret:
                ret.append(res)
        self.lock.release_read()
        return ret

    def set_thread_with_id(self, q_id, thread, queue):
        self.lock.acquire_write()
        self.id_to_queue[q_id] = queue
        self.id_to_thread[q_id] = thread
        self.queue_list.append(queue)
        self.thread_list.append(thread)
        self.lock.release_write()

    def delete_id(self, q_id):
        self.lock.acquire_write()
        del self.id_to_queue[q_id]
        del self.id_to_thread[q_id]
        self.lock.release_write()

    def delete_id_and_check_to_join_thread(self, q_id):
        self.lock.acquire_write()
        thread = None
        if q_id in self.id_to_thread.keys():
            thread = self.id_to_thread[q_id]
            if not thread.is_alive():
                thread.join()
                if thread in self.thread_list:
                    self.thread_list.remove(thread)
            del self.id_to_thread[q_id]
            del self.id_to_queue[q_id]
        self.lock.release_write()

    def join_thread_with_id(self, q_id):
        self.lock.acquire_read()
        thread = self.id_to_thread[q_id]
        self.lock.release_read()
        thread.join()
        self.lock.acquire_write()
        self.thread_list.remove(thread)
        del self.id_to_thread[q_id]
        self.lock.release_write()

    def change_thread_and_queue_of_ids_and_join(self, q_ids, q_id_new_thread):
        self.lock.acquire_write()
        new_thread = self.id_to_thread[q_id_new_thread]
        new_queue = self.id_to_queue[q_id_new_thread]
        for q_id in q_ids:
            thread = self.id_to_thread[q_id]
            if thread in self.thread_list:
                self.thread_list.remove(thread)
                thread.join()
            self.id_to_thread[q_id] = new_thread
            self.id_to_queue[q_id] = new_queue
        self.lock.release_write()

    def change_thread_and_queue_of_ids(self, q_ids, q_id_new_thread):
        self.lock.acquire_write()
        new_thread = self.id_to_thread[q_id_new_thread]
        new_queue = self.id_to_queue[q_id_new_thread]
        for q_id in q_ids:
            self.id_to_thread[q_id] = new_thread
            self.id_to_queue[q_id] = new_queue
        self.lock.release_write()

    def change_thread_and_queue_of_ids_nonblocking(self, q_ids, q_id_new_thread):
        new_thread = self.id_to_thread[q_id_new_thread]
        new_queue = self.id_to_queue[q_id_new_thread]
        for q_id in q_ids:
            self.id_to_thread[q_id] = new_thread
            self.id_to_queue[q_id] = new_queue

    def send_all_threads(self, msg):
        self.lock.acquire_write()
        for p in self.queue_list:
            p.put(msg)
        self.lock.release_write()

    def stop_all_threads(self):
        self.lock.acquire_write()
        for p in self.thread_list:
            p.join()
        self.lock.release_write()

    def stop_shared_dict(self):
        SharedDict.__instance = None
