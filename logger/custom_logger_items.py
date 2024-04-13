import logging

FMT = "{asctime} {name} [{levelname:^7}]:{message}"


class CustomFormatter(logging.Formatter):
    def __init__(self, colors: dict, fmt_string: str):
        super().__init__()
        self.colors = colors
        self.fmt_string = fmt_string
        self.formats = self.create_formats()

    def create_formats(self):
        dc = self.colors["debug"]
        ic = self.colors["info"]
        wc = self.colors["warning"]
        ec = self.colors["error"]
        cc = self.colors["critical"]
        formats = {
            logging.DEBUG: f"\33[38;2;{dc[0]};{dc[1]};{dc[2]}m{self.fmt_string}\33[0m",
            logging.INFO: f"\33[38;2;{ic[0]};{ic[1]};{ic[2]}m{self.fmt_string}\33[0m",
            logging.WARNING: f"\33[38;2;{wc[0]};{wc[1]};{wc[2]}m{self.fmt_string}\33[0m",
            logging.ERROR: f"\33[38;2;{ec[0]};{ec[1]};{ec[2]}m{self.fmt_string}\33[0m",
            logging.CRITICAL: f"\33[38;2;{cc[0]};{cc[1]};{cc[2]}m{self.fmt_string}\33[0m",
        }
        return formats

    def format(self, record):
        log_fmt = self.formats[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


def colored_formatter_factory(level_colors, format_string):
    level_colors = {k: v for d in level_colors for k, v in d.items()}
    return CustomFormatter(level_colors, format_string)


class AddrFilter(logging.Filter):
    """
    оставляем только те логи, с информацией об устройстве 524:56
    if "524:56" in record.msg:
        return record
    """

    def filter(self, record):
        pass