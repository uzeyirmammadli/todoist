from datetime import datetime

from .errors import CommandNotSupported, RequestValidationError, QuitCommandRequest

class Commander:
    _command_types = ["add", "list", "filter", "quit"]

    def __init__(self):
        self._cmd_type = None
    
    @property
    def cmd_type(self):
        return self._cmd_type
    
    @cmd_type.setter
    def cmd_type(self, cmd):
        if cmd not in self._command_types:
            raise CommandNotSupported(f"command {cmd} is not supported")
        else:
            self._cmd_type = cmd

    def route(self):
        cmd = input("Input your command: ")
        self.cmd_type = cmd

        if self.cmd_type == "quit":
            self.handle_quit()
        elif self.cmd_type == "add":
            self.handle_add()
    
    def handle_quit(self):
        raise QuitCommandRequest("quit command initiated")

    def handle_add(self):
        print("Add your new task")
        
        user_input = {}
        user_input["title"] = input("Task title: ")
        user_input["description"] = input("Task description: ")
        user_input["priority"] = input("Set task priority: ")
        user_input["due_date"] = input("Set task due_date: ")

        # add_request = CommandAddRequest(
        #     title = user_input["title"],
        #     description = user_input["description"], 
        #     priority = user_input["priority"],
        #     due_date = user_input["due_date"]
        # )

        add_request = CommandAddRequest(**user_input)
        request_data = add_request.validate()
        print(request_data)

class CommandAddRequest:
    def __init__(self, title, description, priority=None, due_date=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
    

    def validate(self):
        data = {
            "title": self.title,
            "description": self.description
        }

        # Validate priority
        if self.priority is not None and self.priority != "":
            try:
                data["priority"] = int(self.priority)
            except ValueError:
                raise RequestValidationError(f"priority input value {self.priority} is not integer")
        else:
            data["priority"] = None

        # Validate due date
        if self.due_date is not None and self.due_date != "":
            try:
                data["due_date"] = datetime.strptime(self.due_date, "%d-%b-%Y")
            except ValueError as e:
                raise RequestValidationError(f"due_date input value {self.due_date} is not in proper date format")
        else:
            data["due_date"] = None
        
        return data
