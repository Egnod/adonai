class InternalPermission:
    name: str
    description: str = None

    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<InternalPermission | Name: {self.name} | Desc.: {self.description} >"
