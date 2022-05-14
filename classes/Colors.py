from colorama import Fore, Style, init


class Colors:
    def __init__(self, enabled:bool = True):
        if enabled:
            self.TITLE = Fore.LIGHTBLUE_EX + Style.BRIGHT
            self.SUCCESS = Fore.LIGHTGREEN_EX + Style.BRIGHT
            self.WARNING = Fore.LIGHTYELLOW_EX + Style.BRIGHT
            self.ERROR = Fore.LIGHTRED_EX + Style.BRIGHT
            self.SUBTITLE = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
            self.RESET = Fore.RESET + Style.RESET_ALL
            init(autoreset=True)
        else:
            self.TITLE = self.CYAN = self.GREEN = self.YELLOW = self.ERROR = self.MAGENTA = self.RESET = ""
