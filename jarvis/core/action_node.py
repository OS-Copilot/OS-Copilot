class ActionNode:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.code = None
        self.return_val = None
        self.status = False
           
    def __str__(self):
        return f"name: {self.name} \n description: {self.description} \n code: {self.code} \n return: {self.return_val} \n status: {self.status}"
