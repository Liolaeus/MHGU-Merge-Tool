# MHGU-Merge-Tool

Merge Characters from different Monster Hunter Generations Ultimate save files into one.

# Usage

> [!IMPORTANT]
> Before trying to modify your save data, make sure you have a proper backup of your data !

This script takes two save files: `SRC_SAVE` and `DST_SAVE`. And two slots: `SRC_SLOT` and `DST SLOT`.
It will move the character from `SRC_SAVE` in slot `SRC_SLOT` to `DST_SAVE` in `DST_SLOT`, mark `DST_SLOT` as used, and output a `merged_save` file.  

Edit the following variables on top of the script according to your needs:
```Python
# move character slot 1 of `save1` to character slot 3 of `save2`
SRC_FILE = "path/to/save1"
DST_FILE = "path/to/save2"
SRC_SLOT = 1
DST_SLOT = 3
```

Then run 
```
python3 merge.py
```

You can then rename `merged_save` to `system` and move it to your save data location.

# Requirements

- Python3.x
- MHGU `system` save data obtained from your console or emulator

# Credits

This project is based on the work of other people:

- [MHXXSaveEditor](https://github.com/mineminemine/MHXXSaveEditor)
    - [MHXX 'system' file structure](https://github.com/mineminemine/MHXXSaveEditor/wiki/MHXX-'system'-file-structure)
- [MHXXSwitchSaveEditor](https://github.com/Dawnshifter/MHXXSwitchSaveEditor)
