import pylage as pl

from app.layout_test2 import get_app

if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage Layout Dashboard",
        output="index.html",
        serve=True,
        open_browser=True,
    )