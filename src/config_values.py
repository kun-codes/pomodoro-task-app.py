from models.config import app_settings


class ConfigValues:
    BREAK_DURATION = app_settings.get(app_settings.break_duration)
    WORK_DURATION = app_settings.get(app_settings.work_duration)
    LONG_BREAK_DURATION = app_settings.get(app_settings.long_break_duration)
    WORK_INTERVALS = app_settings.get(app_settings.work_intervals)
