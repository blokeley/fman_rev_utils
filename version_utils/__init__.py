import os
from pathlib import Path

from fman import (clipboard, DirectoryPaneCommand, Task,
                  show_status_message, submit_task)
from fman.fs import iterdir, prepare_move
from fman.url import as_human_readable, as_url, basename, join

from .utils import list_obsolete_drafts, released_name

__version__ = '0.3.1'


class SelectObsoleteDrafts(DirectoryPaneCommand):
    def __call__(self):
        pane_url = self.pane.get_path()
        paths = (Path(p) for p in iterdir(pane_url))
        drafts = (str(p) for p in list_obsolete_drafts(paths))

        self.pane.clear_selection()

        for draft in drafts:
            draft_url = join(pane_url, draft)
            self.pane.toggle_selection(draft_url)


class RenameAsReleased(DirectoryPaneCommand):
    def __call__(self):
        selected_urls = self.pane.get_selected_files()

        if not selected_urls:
            # If none have been selected, get the file at the cursor
            selected_urls = [self.pane.get_file_under_cursor()]

        for src_url in selected_urls:
            try:
                src_path = Path(as_human_readable(src_url))
                dest_path = released_name(src_path)
                dest_url = as_url(dest_path)
                submit_task(_Move(src_url, dest_url))

            except ValueError:
                show_status_message('{str(src_path)} is not a draft')


class CopyPathMinusDropbox(DirectoryPaneCommand):
    def __call__(self):
        to_copy = self.get_chosen_files() or [self.pane.get_path()]
        to_copy = [_strip_dbx(as_human_readable(f)) for f in to_copy]
        clipboard.clear()
        clipboard.set_text(os.linesep.join(to_copy))
        _report_clipboard_action('Copied', to_copy,
                                 ' to the clipboard', 'path')


class CopyFileName(DirectoryPaneCommand):
    def __call__(self):
        to_copy = self.get_chosen_files() or [self.pane.get_path()]
        to_copy = [Path(as_human_readable(f)).name for f in to_copy]
        clipboard.clear()
        clipboard.set_text(os.linesep.join(to_copy))
        _report_clipboard_action('Copied', to_copy,
                                 ' to the clipboard', 'path')


class CopyFileStem(DirectoryPaneCommand):
    def __call__(self):
        to_copy = self.get_chosen_files() or [self.pane.get_path()]
        to_copy = [Path(as_human_readable(f)).stem for f in to_copy]
        clipboard.clear()
        clipboard.set_text(os.linesep.join(to_copy))
        _report_clipboard_action('Copied', to_copy,
                                 ' to the clipboard', 'path')


class _Move(Task):

    def __init__(self, src_url, dest_url):
        super().__init__('Moving ' + basename(src_url))
        self.src_url = src_url
        self.dest_url = dest_url

    def __call__(self):
        tasks = list(prepare_move(self.src_url, self.dest_url))
        self.set_size(sum(task.get_size() for task in tasks))
        for task in tasks:
            self.run(task)


def _strip_dbx(path: str) -> str:
    """Removed Dropbox path from beginning of file."""
    prefix = str(Path.home() / 'Dropbox (Springboard)')

    if prefix not in path:
        show_status_message(f'{prefix} not found in {path}', timeout_secs=3)
        return path

    return path.replace(prefix, '', 1).lstrip('\\')


# Copied from
# https://github.com/fman-users/Core/blob/master/core/commands/__init__.py
def _report_clipboard_action(verb, files, suffix='', ftype='file'):
    num = len(files)
    first_file = files[0]
    if num == 1:
        msg = f'{verb} {first_file}{suffix}'
    else:
        plural = 's' if num > 2 else ''
        msg = f'{verb} {first_file} and {num - 1} other ' \
              f'{ftype}{plural}{suffix}'

    show_status_message(msg, timeout_secs=3)
