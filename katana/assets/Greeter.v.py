# Greeter example contract
greeting: public(bytes <=10)

# Constructor
def __init__():
    self.greeting = 'Hello'

# Sets the greeting
def set_greeting(_greeting: bytes <=10):
    self.greeting = _greeting

# Returns the greeting
@constant
def greet() -> bytes <=10:
    return self.greeting