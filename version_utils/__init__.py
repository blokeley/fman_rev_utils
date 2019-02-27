from pathlib import Path

from fman import (DirectoryPaneCommand, Task, show_alert, show_status_message,
                  submit_task)
from fman.fs import iterdir, prepare_move
from fman.url import as_human_readable, as_url, basename, join

from .utils import list_obsolete_drafts, released_name

__version__ = '0.1'


class ListObsoleteDrafts(DirectoryPaneCommand):
    def __call__(self):
        pane_url = self.pane.get_path()
        paths = (Path(p) for p in iterdir(pane_url))
        drafts = (str(p) for p in list_obsolete_drafts(paths))
        show_alert('\n'.join(drafts))


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
