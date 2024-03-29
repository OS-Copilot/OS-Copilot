class ActionNode:
    """
    Represents an action node in a workflow or execution graph, encapsulating details like the action's name, description,
    return value, relevant code snippets, next actions, execution status, and action type.

    Attributes:
        _name (str): The name of the action.
        _description (str): A brief description of what the action does.
        _return_val (str): The value returned by the action upon execution.
        _relevant_code (dict): A dictionary mapping relevant code snippets or references associated with the action.
        _next_action (dict): A dictionary mapping subsequent actions that depend on the current action.
        _status (bool): The execution status of the action, indicating whether it has been successfully executed.
        _type (str): The type of the action, categorizing its purpose or method of execution.
    """
    def __init__(self, name, description, node_type):
        """
        Initializes an instance of the ActionNode class with the given attributes.

        Args:
            name (str): The name of the action.
            description (str): A description of the action.
            type (str): The type of the action.
        """
        self._name = name
        self._description = description
        self._return_val = ''
        self._relevant_code = {}
        self._next_action = {}
        self._status = False
        self._type = node_type

    @property
    def name(self):
        """
        Returns the name of the action.

        Returns:
            str: The action's name.
        """
        return self._name
    
    @property
    def description(self):
        """
        Returns the description of the action.

        Returns:
            str: The action's description.
        """
        return self._description   

    @property
    def return_val(self):
        """
        Returns the return value of the action.

        Returns:
            str: The value returned by the action upon execution.
        """
        return self._return_val
   
    @property
    def relevant_action(self):
        """
        Returns the relevant code snippets or references associated with the action.

        Returns:
            dict: The action's relevant code snippets or references.
        """
        return self._relevant_code
    
    @property
    def status(self):
        """
        Returns the execution status of the action.

        Returns:
            bool: True if the action has been executed successfully, False otherwise.
        """
        return self._status  
    
    @property
    def node_type(self):
        """
        Returns the type of the action.

        Returns:
            str: The action's type.
        """
        return self._type 
    
    @property
    def next_action(self):
        """
        Returns subsequent actions that depend on the current action.

        Returns:
            dict: A mapping of subsequent actions.
        """
        return self._next_action   
    
    def __str__(self):
        """
        Provides a string representation of the ActionNode instance.

        Returns:
            str: A formatted string detailing the action's properties.
        """
        return f"name: {self.name} \n description: {self.description} \n return: {self.return_val} \n relevant_action: {self._relevant_code} \n next_action: {self.next_action} \n status: {self.status} \n type: {self.node_type}"


if __name__ == '__main__':
    node = ActionNode('temp','xxx')
    print(node.name)