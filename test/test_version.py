import os


def test_version():
    """
    Test if __version__ is correctly read from version.txt
    """
    from pathfinding3d import __version__

    # Read the version from version.txt
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "pathfinding3d", "version.txt"), encoding="utf-8"
    ) as file_handler:
        version = file_handler.read().strip()

    assert __version__ == version
