from models.config import app_settings, workspace_specific_settings


class ConfigValues:
    BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.break_duration)
    WORK_DURATION = workspace_specific_settings.get(workspace_specific_settings.work_duration)
    LONG_BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.long_break_duration)
    WORK_INTERVALS = workspace_specific_settings.get(workspace_specific_settings.work_intervals)
    AUTOSTART_WORK = workspace_specific_settings.get(workspace_specific_settings.autostart_work)
    AUTOSTART_BREAK = workspace_specific_settings.get(workspace_specific_settings.autostart_break)
    ENABLE_WEBSITE_FILTER = workspace_specific_settings.get(workspace_specific_settings.enable_website_filter)
    PROXY_PORT = app_settings.get(app_settings.proxy_port)
    CHECK_FOR_UPDATES_ON_START = app_settings.get(app_settings.check_for_updates_on_start)
    HAS_VISITED_TASK_VIEW = app_settings.get(app_settings.has_visited_task_view)
    HAS_VISITED_POMODORO_VIEW = app_settings.get(app_settings.has_visited_pomodoro_view)
    HAS_VISITED_WEBSITE_FILTER_VIEW = app_settings.get(app_settings.has_visited_website_filter_view)
