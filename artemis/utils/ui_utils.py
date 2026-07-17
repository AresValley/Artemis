import os

from artemis.utils.sys_utils import is_windows, is_linux
from artemis.utils.config_utils import CONFIGURE_QT


def set_ui():
    # Style and aspect
    os.environ['QT_QUICK_CONTROLS_STYLE'] = CONFIGURE_QT.value('Controls', 'style', 'Material')
    os.environ['QT_QUICK_CONTROLS_MATERIAL_VARIANT'] = CONFIGURE_QT.value('Material', 'variant', 'Dense')
    os.environ['QT_QUICK_CONTROLS_MATERIAL_THEME'] = CONFIGURE_QT.value('Material', 'theme', 'System')
    os.environ['QT_QUICK_CONTROLS_MATERIAL_ACCENT'] = CONFIGURE_QT.value('Material', 'accent', 'Green')

    # Scaling
    os.environ['QT_SCALE_FACTOR'] = CONFIGURE_QT.value('Scaling', 'factor', '1.00')

    # GUI Backend
    if is_windows():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'

    if is_linux():
        os.environ['QT_QPA_PLATFORM'] = 'wayland;xcb'

    # Optimizations and workarounds
    os.environ['QT_ENABLE_GLYPH_CACHE_WORKAROUND'] = '1'
    os.environ['QML_USE_GLYPHCACHE_WORKAROUND'] = '1'

    # Debug and loggings
    debug = CONFIGURE_QT.value('Develop', 'debug', '0')

    os.environ['QT_DEBUG_PLUGINS'] = CONFIGURE_QT.value('Develop', 'debug_plugin', '0')

    if debug != '1':
        os.environ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg*=false"
