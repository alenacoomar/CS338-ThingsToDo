import traceback

from application import app,db,manager
from flask_script import Server, Command
from www import *

manager.add_command("runserver",Server(host="0.0.0.0", use_debugger=True, use_reloader=True))

@Command
def create_all():
    from application import db
    from common.models.user import User
    db.create_all()

def main():
    manager.run()

manager.add_command("create_all",create_all)
if __name__ == "__main__":
    from common.models.user import User
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()