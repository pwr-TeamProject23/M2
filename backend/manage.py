import argparse

from src.auth.repositories import UserRepository


def create_admin(email: str, password: str):
    UserRepository.create_super_user(email, password)
    print(f"Created admin user with email {email} and password {password}")

def main():
    parser = argparse.ArgumentParser(description="App management script")
    parser.add_argument("action", choices=["create_admin"], help="Action to perform")

    parser.add_argument("--email", required=True, help="Admin email")
    parser.add_argument("--password", required=True, help="Admin password")

    args = parser.parse_args()

    if args.action == "create_admin":
        create_admin(args.email, args.password)
    else:
        print("Invalid action. Supported actions: create_admin")

if __name__ == "__main__":
    main()