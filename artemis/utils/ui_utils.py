import os

from artemis.utils.sys_utils import is_windows, is_linux, is_macos
from artemis.utils.config_utils import CONFIGURE_QT


def set_ui():
    os.environ['QT_QUICK_CONTROLS_STYLE'] = CONFIGURE_QT.get_or_default('Controls', 'style', 'Material')
    os.environ['QT_QUICK_CONTROLS_MATERIAL_VARIANT'] = CONFIGURE_QT.get_or_default('Material', 'variant', 'Dense')
    os.environ['QT_QUICK_CONTROLS_MATERIAL_THEME'] = CONFIGURE_QT.get_or_default('Material', 'theme', 'System')
    os.environ['QT_QUICK_CONTROLS_MATERIAL_ACCENT'] = CONFIGURE_QT.get_or_default('Material', 'accent', 'Green')

    if is_windows():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'

    if is_linux():
        os.environ['GDK_BACKEND'] = 'x11'
        os.environ['QT_QPA_PLATFORM'] = 'xcb'

    os.environ['QT_ENABLE_GLYPH_CACHE_WORKAROUND'] = '1'
    os.environ['QML_USE_GLYPHCACHE_WORKAROUND'] = '1'
