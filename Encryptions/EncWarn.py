import warnings
class NoSetKeyWarning(UserWarning):
    "not setting key warnings based by :obj:`UserWarning`"
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        return None
    @staticmethod
    def ignore():
        return warnings.simplefilter("ignore",NoSetKeyWarning)
