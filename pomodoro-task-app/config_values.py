from models.config import workspace_specific_settings


class ConfigValues:
    BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.break_duration)
    WORK_DURATION = workspace_specific_settings.get(workspace_specific_settings.work_duration)
    LONG_BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.long_break_duration)
    WORK_INTERVALS = workspace_specific_settings.get(workspace_specific_settings.work_intervals)
    AUTOSTART_WORK = workspace_specific_settings.get(workspace_specific_settings.autostart_work)
    AUTOSTART_BREAK = workspace_specific_settings.get(workspace_specific_settings.autostart_break)

