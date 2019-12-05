
def getter_setter_gen(attr, typ):
    def getter(self):
        return getattr(self, "__" + attr)

    def setter(self, value):
        if not isinstance(value, typ):
            raise TypeError("{} attribute must be of type {}".format(attr, typ))
        object.__setattr__(self, "__" + attr, value)
    return property(getter, setter)

# function to validate the user input type
def check_attribute(clas):
    attr_dict = {}
    for key, value in clas.__dict__.items():
        if isinstance(value, type):
            value = getter_setter_gen(key, value)
        attr_dict[key] = value
    # Creates a new class using the modified dictionary as the class dictionary:
    return type(clas)(clas.__name__, clas.__bases__, attr_dict)

