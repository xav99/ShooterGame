class CExceptions(Exception):
    def __init__(self, *args):
        self.name = self.myname()
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.name + ' ' + f'{self.message}'  # comma between selfTargetException and f crashes program
        else:
            return self.name + " has been raised"

    def myname(self):
        return self.__class__.__name__

'''
class CombatExceptions:
    class SelfTargetException(CExceptions):
        def __init__(self, *args):
            super().__init__(*args)

    class NoTargetSelected(CExceptions):
        def __init__(self, *args):
            super().__init__(*args)
'''


class StandardExceptions:
    class InvalidGameMode(CExceptions):
        def __init__(self, *args):
            super().__init__(*args)

    class InvalidOperationException(CExceptions):
        def __init__(self, *args):
            super().__init__(*args)
