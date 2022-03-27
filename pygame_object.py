class PygameImageLayer:
    def init(self, type, is_array, parameters, priority):
        self.type = type
        self.is_array = is_array
        self.parameters = parameters
        self.priority = priority
    
    def spread_details(self):
        if not self.is_array:
            return self.parameters
        else:
            for layer in self.parameters:
                return 
        