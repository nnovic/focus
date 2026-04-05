#!/usr/bin/env python3
"""
Interactive CLI tool for managing passwords in the system keyring.

Usage:
    python keyring_cli.py

Commands:
    get     - Retrieve a password
    set     - Store a password
    delete  - Delete a password
    list    - List stored credentials (service/username pairs)
    help    - Show this help
    exit    - Exit the program
"""

import keyring
import sys


def print_menu():
    """Print the main menu"""
    print("\n" + "=" * 60)
    print("KEYRING PASSWORD MANAGER")
    print("=" * 60)
    print("1. get     - Retrieve a password")
    print("2. set     - Store a password")
    print("3. delete  - Delete a password")
    print("4. list    - List all stored credentials")
    print("5. help    - Show help")
    print("6. exit    - Exit")
    print("=" * 60)


def get_password():
    """Get a password from keyring"""
    print("\n--- GET PASSWORD ---")
    service = input("Service name: ").strip()
    username = input("Username: ").strip()

    if not service or not username:
        print("✗ Service and username are required")
        return

    password = keyring.get_password(service, username)

    if password:
        print(f"✓ Password for {service}/{username}:")
        print(f"  {password}")
    else:
        print(f"✗ No password found for {service}/{username}")


def set_password():
    """Store a password in keyring"""
    print("\n--- SET PASSWORD ---")
    service = input("Service name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not service or not username or not password:
        print("✗ All fields are required")
        return

    keyring.set_password(service, username, password)
    print(f"✓ Password stored for {service}/{username}")


def delete_password():
    """Delete a password from keyring"""
    print("\n--- DELETE PASSWORD ---")
    service = input("Service name: ").strip()
    username = input("Username: ").strip()

    if not service or not username:
        print("✗ Service and username are required")
        return

    # Confirm deletion
    confirm = input(f"Delete password for {service}/{username}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("✗ Deletion cancelled")
        return

    try:
        keyring.delete_password(service, username)
        print(f"✓ Password deleted for {service}/{username}")
    except Exception as e:
        print(f"✗ Failed to delete password: {e}")


def list_credentials():
    """
    List all stored credentials.

    Note: This is a simple simulation. The actual keyring backend may not expose
    a list method, so this shows a demonstration of common services.
    """
    print("\n--- LIST CREDENTIALS ---")
    print("Note: Full credential listing depends on keyring backend support.")
    print("\nCommon services to check:")

    common_services = [
        ("gitlab", ["alice", "bob", "user@company.com"]),
        ("jira", ["alice", "bob"]),
        ("github", ["alice-dev", "bob-dev"]),
        ("bitbucket", ["alice"]),
    ]

    found_any = False

    for service, usernames in common_services:
        for username in usernames:
            password = keyring.get_password(service, username)
            if password:
                print(f"  ✓ {service}/{username}")
                found_any = True

    if not found_any:
        print("  (No credentials found in common services)")

    # Allow user to manually specify service to check
    print("\nSearch for a specific service:")
    service = input("Service name (or press Enter to skip): ").strip()
    if service:
        print(f"Checking {service}...")
        # Since we can't enumerate usernames, we'll just show some common ones
        test_usernames = ["admin", "user", "alice", "bob", "default"]
        found = False
        for username in test_usernames:
            password = keyring.get_password(service, username)
            if password:
                print(f"  ✓ {service}/{username}")
                found = True
        if not found:
            print(f"  No credentials found for {service}")


def show_help():
    """Show help information"""
    print("\n" + "=" * 60)
    print("HELP")
    print("=" * 60)
    print("""
GET PASSWORD:
  Retrieves a stored password from the keyring.
  You'll be prompted for the service name and username.

SET PASSWORD:
  Stores a new password in the keyring.
  You'll be prompted for the service name, username, and password.
  If the password already exists, it will be overwritten.

DELETE PASSWORD:
  Removes a password from the keyring.
  You'll be asked to confirm before deletion.

LIST CREDENTIALS:
  Shows stored credentials. This checks common services
  and allows you to search for a specific service.

KEYRING BACKEND:
  Your system uses: {backend}
  Backend class: {backend_class}

EXAMPLES:
  Service: gitlab, Username: alice
  Service: jira, Username: alice@company.com
  Service: github, Username: alice-dev
""".format(
        backend=keyring.get_keyring(),
        backend_class=type(keyring.get_keyring()).__name__
    ))


def main():
    """Main interactive loop"""
    print("\n" + "=" * 60)
    print("KEYRING PASSWORD MANAGER")
    print("=" * 60)
    print(f"Current backend: {type(keyring.get_keyring()).__name__}")
    print("Type 'help' for commands or press Ctrl+C to exit")

    while True:
        try:
            print_menu()
            choice = input("Choose an option (1-6) or type command: ").strip().lower()

            if choice in ["1", "get"]:
                get_password()
            elif choice in ["2", "set"]:
                set_password()
            elif choice in ["3", "delete"]:
                delete_password()
            elif choice in ["4", "list"]:
                list_credentials()
            elif choice in ["5", "help"]:
                show_help()
            elif choice in ["6", "exit", "quit"]:
                print("\n✓ Goodbye!")
                sys.exit(0)
            else:
                print("✗ Invalid choice. Please try again.")

        except KeyboardInterrupt:
            print("\n\n✓ Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
