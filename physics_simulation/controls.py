class KeyControls:
    """
    An interface for controlling app functionality via key-presses. 
    Create a Controls instance, bind functions to keys, and then 
    have Controls handle key presses. 
    """
    
    def __init__(self, name="Controls", help_key='h', help_message="show this help message"):
        self.name = name
        self.press_bindings = {}
        self.release_bindings = {}
        if help_key:
            self.bind_press(help_key, help_message, self.show_help)
    
    def bind_press(self, _key, help, function):
        "Binds a key [ress to a function. In other words, when the key is pressed, the function will be called."
        self.press_bindings[_key] = (help, function)
        
    def bind_release(self, _key, help, function):
        "Binds a key release to a function. In other words, when the key is released, the function will be called."
        self.release_bindings[_key] = (help, function)
        
    def handle_press(self):
        "Calls the function bound to a key press, if the key is bound."
        if key in self.press_bindings.keys():
            help, function = self.press_bindings[key]
            function()
            
    def handle_release(self):
        "Calls the function bound to a key release, if the key is bound."
        if key in self.release_bindings.keys():
            help, function = self.release_bindings[key]
            function()
            
    def show_help(self):
        "Prints out the help message"
        print(self)
        
    def keyname(self, k):
        "Provides the name of the key, which is usually just the key itself"
        if k == ' ':
            return 'space'
        return k
            
    def __str__(self):
        "The string representation of the controls."
        bindings = (
           [(k, "press", help) for k, (help, fn) in self.press_bindings.items()] + 
           [(k, "release", help) for k, (help, fn) in self.release_bindings.items()]
        )
        return "\n".join(
            [self.name] + 
            ["  {} {}: {}".format(event, self.keyname(k), help) for k, event, help in sorted(bindings)]
        )
        
