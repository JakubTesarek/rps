from controler import Controler
from view import View


if __name__ == '__main__':
    controler = Controler()
    view = View(controler)
    view.run()
