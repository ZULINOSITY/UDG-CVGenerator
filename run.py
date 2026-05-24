import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
dlls_path = os.path.join(base_dir, "dlls")


if sys.platform == 'win32' and os.path.exists(dlls_path):
    os.add_dll_directory(dlls_path)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)