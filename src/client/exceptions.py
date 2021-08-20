class NetworkSelectionError(Exception):
    def __init__(
        self,
        message="Network isn't selected: can't retrieve data. Please select a network first.",
    ):
        self.message = message
        super().__init__(self.message)
