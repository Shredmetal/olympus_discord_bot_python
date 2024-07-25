from typing import Literal, Callable
from src.buttons.base_view import BaseView


def lazy_import(module_name: str, class_name: str) -> Callable:
    def _import():
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)

    return _import


InitialView = lazy_import('src.buttons.logs_view', 'InitialView')
CommonIssuesListView = lazy_import('src.buttons.common_issues_buttons.common_issues_list_view', 'CommonIssuesListView')


def create_base_view(view_type: Literal["initial", "common_issues", "combined"],
                     log_status: Literal["normal", "no_logs"] = "normal") -> BaseView:
    if view_type == "initial":
        return InitialView()()
    elif view_type == "common_issues":
        return CommonIssuesListView()(log_status=log_status)
    elif view_type == "combined":
        view = InitialView()()
        common_issues_view = CommonIssuesListView()(log_status=log_status)
        common_issues_button = common_issues_view.common_issues_button
        view.add_item(common_issues_button)
        return view
    else:
        raise ValueError(f"Invalid view_type: {view_type}")
