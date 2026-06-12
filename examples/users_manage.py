"""Create and configure a TestStand user, then check its credentials and privileges.

Builds a User object with the Engine, sets its login name, full name, and
password, validates the password, and queries privileges with User.has_privilege
using the UserPrivilege names. Everything happens in memory; this does not modify
the station's Users.ini.

In TestStand, effective privileges usually come from the group a user belongs to
(Operator, Technician, Developer, ...), configured in the station Users file, so
this example focuses on creating/configuring a user and querying privileges
rather than granting them.

Demonstrates:
- Creating a user with Engine.new_user
- Setting User.login_name / full_name / password
- Checking credentials with User.validate_password
- Querying privileges with User.has_privilege and the UserPrivilege names
"""

from __future__ import annotations

from py_teststand import Engine, UserPrivilege


def main() -> None:
    with Engine() as engine:
        user = engine.new_user()
        user.login_name = "operator1"
        user.full_name = "Test Operator"
        user.password = "ts-secret"

        print(f"User: {user.login_name} ({user.full_name})")
        print(f"  password 'ts-secret' valid: {user.validate_password('ts-secret')}")
        print(f"  password 'wrong' valid:     {user.validate_password('wrong')}")

        print("  privilege checks:")
        for privilege in (
            UserPrivilege.Operate,
            UserPrivilege.Execute,
            UserPrivilege.Develop,
            UserPrivilege.Debug,
            UserPrivilege.EditUsers,
        ):
            print(f"    {privilege.value:18} {user.has_privilege(privilege.value)}")


if __name__ == "__main__":
    main()
