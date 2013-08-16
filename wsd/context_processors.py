# coding=utf-8

from . import app

@app.context_processor
def utility_processor():
    def get_static(path, static_dir=app.static_folder):
        import os

        f = os.path.join(static_dir, path)
        return "{root}/{path}?v={token}".format(root=app.static_url_path, path=path, token=int(os.stat(f).st_mtime))

    return dict(get_static=get_static)