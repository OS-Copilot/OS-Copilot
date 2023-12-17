class ActionNode:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.code = None
        self.return_val = None
        self.status = False

    @property
    def name(self):
        return self.name
    
    @property
    def description(self):
        return self.description
    
    @property
    def code(self):
        return self.code    

    @property
    def return_val(self):
        return self.return_val
    
    @property
    def status(self):
        return self.status  
    
    def __str__(self):
        return f"name: {self.name} \n description: {self.description} \n code: {self.code} \n return: {self.return_val} \n status: {self.status}"
