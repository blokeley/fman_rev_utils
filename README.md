# fman_rev_utils

Revision control utilities for the [fman](https://fman.io/) file manager.

See the [fman plugin documentation](https://fman.io/docs/plugins-introduction) for more 
information.

## Filename conventions

The filenames should have "revA1" or "revA2" etc. for a draft and "revA" or revB" etc. for 
released files.

## Utilities provided by this plugin

* Select obsolete drafts.  This selects files in the current pane which have released files.  
  For example, if a pane has revA1, revA2 and revA, then revA1 and revA2 would be highlighted.
  
* List obsolete drafts.  As above but list filenames in a dialog box.

* Rename as released.  Rename revA1 to revA etc.

* Copy file name.  Copies the file names of the selected files to the clipboard.

* Copy file stem.  Copies the file stems (file name without the suffix) of the selected files to 
  the clipboard.

* Copy path minus Dropbox.  Copies the paths of the selected files, without the Dropbox path, to
  the clipboard.

* Copy path, replacing your user name with %username% so that hyperlinks should work on their
  computers.
