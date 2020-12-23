

# all data and logic that is shared between modules
"""
Python provides a very straightforward packaging system, which is simply an extension of the module mechanism to a directory.

Any directory with an __init__.py file is considered a Python package. The different modules in the package are imported in a similar manner as plain modules, but with a special behavior for the __init__.py file, which is used to gather all package-wide definitions.

A file modu.py in the directory pack/ is imported with the statement import pack.modu. This statement will look for __init__.py file in pack and execute all of its top-level statements. Then it will look for a file named pack/modu.py and execute all of its top-level statements. After these operations, any variable, function, or class defined in modu.py is available in the pack.modu namespace.

A commonly seen issue is adding too much code to __init__.py files. When the project complexity grows, there may be sub-packages and sub-sub-packages in a deep directory structure. In this case, importing a single item from a sub-sub-package will require executing all __init__.py files met while traversing the tree.

Leaving an __init__.py file empty is considered normal and even good practice, if the package’s modules and sub-packages do not need to share any code.

Lastly, a convenient syntax is available for importing deeply nested packages: import very.deep.module as mod. This allows you to use mod in place of the verbose repetition of very.deep.module.
"""