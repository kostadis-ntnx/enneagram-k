This directory is only a template seed location for wiki markdown files.

Per-repo canonical wiki content should live outside the tooling repository and
be configured with:

  ennegram_cli.py init --data-root /path/to/data --wiki-root /path/to/wiki

If a newly configured wiki root is empty, init can seed it from markdown files
in this directory.
