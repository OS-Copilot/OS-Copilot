class ActionNode:
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._code = ''
        self._return_val = ''
        self._relevant_action = {}
        self._status = False

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
        return self._relevant_action
    
    @property
    def status(self):
        return self._status  
    
    def __str__(self):
        return f"name: {self.name} \n description: {self.description} \n code: {self.code} \n return: {self.return_val} \n status: {self.relevant_action} \n status: {self.status}"


if __name__ == '__main__':
    node = ActionNode('dzc','xxx')
    print(node.name)