import hmac

class HashingService:
    def __init__(self, data, hashkey, algorithm):
        self.data = data
        self.hashkey = hashkey
        self.algorithm = algorithm
        
    def get_hashed_data(self):
        hashed_data = hmac.new(self.hashkey.encode('utf-8'), self.data.encode('utf-8'), self.algorithm).hexdigest()
        return hashed_data