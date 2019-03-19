import re


RELEASED_REGEX = re.compile(r'.*rev[A-Z]+\D.*')
DRAFT_REGEX = re.compile(r'(.*rev[A-Z]+)\d+(.*)')


def list_obsolete_drafts(paths):
    """List the obsolete drafts (ones which have a released version).

    Parameters:
    path is the path to search
    list_func is the function to call to list the files like os.listdir()

    Returns:
    list of obsolete paths
    """
    drafts = []
    releases = []
    obsolete_drafts = []

    for path in paths:
        if DRAFT_REGEX.match(path.name):
            drafts.append(path)

        elif RELEASED_REGEX.match(path.name):
            releases.append(path)

    for draft in drafts:
        if is_obsolete(draft, releases):
            obsolete_drafts.append(draft)

    return obsolete_drafts


def is_obsolete(path, releases):
    """Return True if path is a draft with a released version,
    otherwise False.
    """
    return released_name(path) in releases


def released_name(draft_path):
    draft_match = DRAFT_REGEX.match(draft_path.name)

    if not draft_match:
        raise ValueError(f'{draft_path} is not a draft')

    released_name_ = ''.join(draft_match.groups())
    return draft_path.with_name(released_name_)
