import argparse

from src.auth.database import UserManager


def create_admin():
    UserManager.create_super_user()
    print("Created admin user")

def main():
    parser = argparse.ArgumentParser(description="App managment script")
    parser.add_argument("action", choices=["create_admin"], help="Action to perform")

    args = parser.parse_args()

    if args.action == "create_admin":
        create_admin()
    else:
        print("Invalid action. Supported actions: create_admin")

if __name__ == "__main__":
    main()