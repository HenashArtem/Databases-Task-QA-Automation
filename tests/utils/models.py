class Models:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_data(self, value):
        return str(getattr(self, value))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
