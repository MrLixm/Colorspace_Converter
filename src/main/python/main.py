import sys

from  PySide2 import QtGui
from fbs_runtime.application_context.PySide2 import ApplicationContext, cached_property

from package.main_window import MainWindow


class AppContext(ApplicationContext):
    def run(self):
        main_window = MainWindow(ctx=self)
        main_window.resize(1200, 750)
        main_window.show()
        return self.app.exec_()


if __name__ == '__main__':
    appctxt = AppContext()  # 1. Instantiate ApplicationContext
    sys.exit(appctxt.run())
