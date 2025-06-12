UserStore
=========

The `UserStore` class is responsible for managing user authentication within the AGROSMART application. It handles user data storage, verification, and initialization of default user credentials.

Class Definition
----------------

.. autoclass:: UserStore
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

### `__init__(self)`

Initializes the `UserStore` instance. It sets up the path for the users file and initializes the user data file with default credentials if it does not exist.

### `_init_users_file(self)`

Private method that checks if the users file exists. If not, it creates the file with a default user (admin) and a hashed password.

### `verify_user(self, username, password)`

Verifies the provided username and password against the stored user data. Returns `True` if the credentials are valid, otherwise returns `False`.

Parameters:
- `username` (str): The username of the user attempting to log in.
- `password` (str): The password provided by the user.

Returns:
- bool: `True` if the user is verified, `False` otherwise.