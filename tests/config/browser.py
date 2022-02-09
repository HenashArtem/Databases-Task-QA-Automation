class BrowserConfig(object):
    BROWSER = "chrome"
    CHROME_VERSION = "75.0"
    FIREFOX_VERSION = "66.0"


class Grid(object):
    USE_GRID = False
    GRID_HOST = "localhost"
    GRID_PORT = "5565"
    GRID_URL = "http://{host}:{port}/wd/hub"
    IS_VNC_ENABLED = True
    IS_VIDEO_ENABLED = False
