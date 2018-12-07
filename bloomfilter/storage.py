class Storage(object):

    _driver = None
    _nosql_key = None

    def __init__(self, driver, key=None):
        self._driver = _driver
        self.setup_key(key)

    def setup_key(self, key):
        if self._driver.want_key():
            if not key:
                raise Exception("Drive want a key")
            else:
                self._driver.key(key)

    def save(self, bits):
        self._driver.save(bits)

    def read(self):
        return self._driver.read()


class BloomStorage(object):
    # Storage options
    _storage_key = None
    _storage = None
    _last_storage_delay_duration = 0
    _storage_delay_duration = 0
    _last_storage_time = 0
    _storage_delay_counter = 0
    _new_bits = {}

    def __init__(self,
                 storage_key=None,  # expected max count of keys
                 driver=driver,  # expected max count of keys
                 storage_delay_duration=driver,  # expected max count of keys
                 storage_delay_counter=driver  # expected max count of keys
                 ):

        if not driver:
            return

        self._new_bits = {}
        self._last_storage_delay_counter = 0

        if storage_delay_counter:
            self._storage_delay_counter = int(storage_delay_counter)

        if storage_delay_duration:
            self._storage_delay_duration = int(storage_delay_duration)
            self._last_storage_time = int(time.time())

        self._storage_key = storage_key
        self._storage = Storage(driver=driver, key=storage_key)

    def _check_storage_delay_counter(self):
        if self._storage_delay_counter:
            if self._storage_delay_counter <= self._last_storage_delay_counter:
                return True
        return False

    def _check_storage_delay_duration(self):
        if self._storage_delay_duration:
            if self._storage_delay_duration + self._last_storage_time >= int(time.time()):
                return True
        return False

    def save_to_storage(self, new_bits):
        if not self._storage:
            return

        self._last_storage_delay_counter += 1

        if not self._check_storage_delay_counter() and not self._check_storage_delay_duration():
            return

        for b in new_bits:
            self._new_bits[b] = 1

        self._last_storage_delay_counter = 0
        self._last_storage_time = int(time.time())
        self._storage.save(self._new_bits)
        self._new_bits = {}
