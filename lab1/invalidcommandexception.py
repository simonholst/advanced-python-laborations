class InvalidCommandException(Exception):

    def __init__(self, command):
        self.invalid_command = command
        super().__init__('Invalid command: ' + command)
