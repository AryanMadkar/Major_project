class BoundedCache(dict):
    """
    Size-bounded cache to prevent memory leaks from unbounded dictionary growth.
    """
    def __init__(self, max_size=500):
        super().__init__()
        self.max_size = max_size
        self.keys_list = []

    def __setitem__(self, key, value):
        if key not in self:
            self.keys_list.append(key)
        super().__setitem__(key, value)
        if len(self) > self.max_size:
            oldest_key = self.keys_list.pop(0)
            self.pop(oldest_key, None)

embedding_cache = BoundedCache(max_size=500)