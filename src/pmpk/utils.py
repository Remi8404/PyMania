class SingletonMeta(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs): # type: ignore
        if cls not in cls._instances: # type: ignore
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]