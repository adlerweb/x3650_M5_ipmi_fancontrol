#/bin/bash

SWD=$(dirname "${BASH_SOURCE[0]}")

if [[ -f "$SWD/pyvenv.cfg" && -f "$SWD/bin/activate" ]]; then
    . "$SWD/bin/activate"
fi

python "$SWD/ipmi_fancontrol.py" "$@"