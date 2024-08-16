from glob import glob
from pathlib import Path
import os
import platform
from typing import List, Union, Optional

if platform.system() == 'Windows':

    SEARCH_DIRECTORIES = [
        'C:\Windows\System32'
    ]

    search_pattern = 'CAENHVWrapper.dll'

elif platform.system() == 'Linux':
    SEARCH_DIRECTORIES = [
        '/lib', '/lib64', '/usr/lib', '/usr/lib64', '/usr/local/lib',
        '/usr/local/lib64', '~/local/lib', '~/local/lib64'
    ]

    search_pattern = 'libcaenhvwrapper.so*'

else:
    print('Operating system not supported')



def find_dll(
        extra_dirs: Optional[List[Union[str,
                                        Path]]] = None) -> Union[Path, None]:
    """ Search for CAENHVWrapper in known places
    """
    _search_dirs = SEARCH_DIRECTORIES + []
    if os.environ.get('LD_LIBRARY_PATH', None):
        _search_dirs += os.environ['LD_LIBRARY_PATH'].split(':')
    if extra_dirs:
        if isinstance(extra_dirs, str):
            extra_dirs = list(extra_dirs)
        _search_dirs += extra_dirs
    _search_dirs = set(_search_dirs)
    candidates = []
    for _dir in _search_dirs:
        _dir = Path(_dir)
        if _dir.exists():
            search_path = str(_dir / search_pattern)
            # print(f"Going to search {search_path}")
            for filename in glob(search_path):
                return Path(filename)


if __name__ == '__main__':
    print("Found CAENHVWrapper library in", find_dll())
