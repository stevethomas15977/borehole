class Attribute:
    def __init__(self, name, key, value):
        self._name = name
        self._key = key
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"Attribute(name={self._name}, key={self._key}, value={self._value})"