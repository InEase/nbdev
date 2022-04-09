# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/06_clean.ipynb.

# %% auto 0
__all__ = ['clean_nb', 'nbdev_clean_nbs']

# %% ../nbs/06_clean.ipynb 3
from fastcore.script import *
from fastcore.utils import *
from fastcore.imports import *

from .imports import *
from .read import *
from .sync import *

# %% ../nbs/06_clean.ipynb 7
def _clean_cell_output(cell):
    "Remove execution count in `cell`"
    if 'outputs' in cell:
        for o in cell['outputs']:
            if 'execution_count' in o: o['execution_count'] = None
            o.get('data',{}).pop("application/vnd.google.colaboratory.intrinsic+json", None)
            o.get('metadata', {}).pop('tags', None)

# %% ../nbs/06_clean.ipynb 8
def _clean_cell(cell, clear_all=False):
    "Clean `cell` by removing superfluous metadata or everything except the input if `clear_all`"
    if 'execution_count' in cell: cell['execution_count'] = None
    if 'outputs' in cell:
        if clear_all: cell['outputs'] = []
        else:         _clean_cell_output(cell)
    if cell['source'] == ['']: cell['source'] = []
    cell['metadata'] = {} if clear_all else {
        k:v for k,v in cell['metadata'].items() if k=="hide_input"}

# %% ../nbs/06_clean.ipynb 9
def clean_nb(nb, clear_all=False):
    "Clean `nb` from superfluous metadata"
    for c in nb['cells']: _clean_cell(c, clear_all=clear_all)
    nb['metadata'] = {k:v for k,v in nb['metadata'].items() if k in
                     ("kernelspec", "jekyll", "jupytext", "doc")}

# %% ../nbs/06_clean.ipynb 12
def _wrapio(strm): return io.TextIOWrapper(strm, encoding='utf-8', line_buffering=True)

def _clean_write(nb, f_in, f_out=None, clear_all=False):
    if not f_out: f_out = f_in
    nb = json.load(f_in)
    clean_nb(nb, clear_all=clear_all)
    write_nb(nb, f_out)

# %% ../nbs/06_clean.ipynb 13
@call_parse
def nbdev_clean_nbs(
    fname:str=None, # A notebook name or glob to convert
    clear_all:bool_arg=False, # Clean all metadata and outputs
    read_stdin:bool_arg=False # Read input stream and not nb folder
):
    "Clean all notebooks in `fname` to avoid merge conflicts"
    # Git hooks will pass the notebooks in stdin
    if read_stdin: return _clean_write(nb, _wrapio(sys.stdin), _wrapio(sys.stdout), clear_all=clear_all)

    if fname is None: fname = get_config().path("nbs_path")
    for f in globtastic(fname, file_glob='*.ipynb', skip_folder_re='^[_.]'):
        _clean_write(nb, f, clear_all=clear_all)
