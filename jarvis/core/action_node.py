class ActionNode:
    def __init__(self, name, description, type):
        self._name = name
        self._description = description
        self._code = ''
        self._return_val = ''
        self._relevant_code = {}
        self._next_action = {}
        self._status = False
        self._type = type

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def code(self):
        return self._code    

    @property
    def return_val(self):
        return self._return_val
   
    @property
    def relevant_action(self):
        return self._relevant_code
    
    @property
    def status(self):
        return self._status  
    
    @property
    def type(self):
        return self._type 
    
    @property
    def next_action(self):
        return self._next_action   
    
    def __str__(self):
        return f"name: {self.name} \n description: {self.description} \n code: {self.code} \n return: {self.return_val} \n relevant_action: {self._relevant_code} \n next_action: {self.next_action} \n status: {self.status} \n type: {self.type}"


if __name__ == '__main__':
    node = ActionNode('dzc','xxx')
    print(node.name)