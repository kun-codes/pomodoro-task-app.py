from models.config import app_settings


class ConfigValues:
    BREAK_DURATION = app_settings.get(app_settings.break_duration)
    WORK_DURATION = app_settings.get(app_settings.work_duration)
    LONG_BREAK_DURATION = app_settings.get(app_settings.long_break_duration)
    WORK_INTERVALS = app_settings.get(app_settings.work_intervals)
    AUTOSTART_WORK = app_settings.get(app_settings.autostart_work)
    AUTOSTART_BREAK = app_settings.get(app_settings.autostart_break)

