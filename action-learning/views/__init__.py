from .action import ActionCoachView, ActionCompareView
from .fitness import FitnessView
from .multiple import MultipleView



def setup_routes(app):
    app.router.add_view("/fitness/{activity}/", FitnessView)
    app.router.add_view("/multipleperson/", MultipleView)
    app.router.add_view("/action/coach/", ActionCoachView)
    app.router.add_view("/action/compare/", ActionCompareView)
   