# Contributing to **pathfinding3D**

Please inform the maintainer as early as possible about your planned
feature developments, extensions, or bugfixes that you are working on.
An easy way is to open an issue or a pull request in which you explain
what you are trying to do.

Before starting your work, please check the existing issues and discussions to avoid duplicate efforts. Engaging in discussions on issues can provide better clarity and enhance community interaction.

## Pull Requests

The preferred way to contribute to *pathfinding3D* is to fork the main repository on Github, then submit a "pull request" (PR). Follow this checklist before submitting your PR:

1. Fork the [project repository](https://github.com/harisankar95/pathfinding3D):
   click on the ``Fork`` button near the top of the page. This creates a copy of
   the code under your namespace on the Github servers.

2. Clone this repository to your local disk:

   ```bash
   git clone git@github.com:YourLogin/pathfinding3D.git
   cd pathfinding3D
   ```

3. Prepare the development environment:

   ```bash
   pip install numpy pytest sphinx
   ```

4. Create a new branch to hold your changes, for example (replace
   ``my-feature`` with a short but descriptive name of your feature, bugfix, etc.):

   ```bash
   git checkout -b my-feature
   ```

   and start making changes.

5. When you're done making changes, add changed files to the index with ``git add`` and
   ``git commit`` them with a descriptive message.

   ```bash
   git add modified_files
   git commit -m "A short description of the commit"
   ```

6. Run the tests with ``pytest``. If they pass, you are ready to submit a pull request.

   ```bash
   pytest test
   ```

7. Push your changes to Github with:

   ```bash
   git push -u origin my-feature
   ```

Finally, go to the web page of your fork of the repo,
and click ``Pull request`` to send your changes to the maintainers for review.

## Merge Policy

Summary: maintainer can push minor changes directly, pull request + 1 reviewer for everything else.

Usually, direct push to the main branch of pathfinding3D is restricted. Only minor changes, urgent bugfixes, and maintenance commits can be pushed directly to the main branch by the maintainer without a review. "Minor" implies backwards compatibility and successful completion of all tests. No new features must be added.

Developers should submit pull requests for their changes. PRs should be reviewed by at least one other developer and merged by the maintainer. New features must be documented and tested. Breaking changes must be discussed and announced in advance with deprecation warnings.

Contributors are encouraged to engage in the feedback and review process. If you haven't received any response on your PR within a reasonable timeframe, feel free to reach out for an update.

All contributions will be acknowledged, either through mentions in release notes, the contributor list, or other appropriate channels.

By following these guidelines, you help maintain the quality and consistency of the pathfinding3D project. We appreciate your contributions and look forward to your active participation in our community.
