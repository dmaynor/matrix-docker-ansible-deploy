#!/usr/bin/env python3
"""
Fix locale issues in Nix environments
"""
import os
import subprocess
import sys
from pathlib import Path


def find_glibc_locales():
    """Find the glibc-locales path in the Nix store"""
    try:
        # Try to find the glibc-locales in the Nix store
        result = subprocess.run(
            ["nix-build", "<nixpkgs>", "-A", "glibcLocales", "--no-out-link"],
            capture_output=True,
            text=True,
            check=True
        )
        locale_path = result.stdout.strip()
        return f"{locale_path}/lib/locale/locale-archive"
    except subprocess.CalledProcessError:
        return None


def update_envrc(envrc_path, locale_archive_path):
    """Update .envrc with locale settings"""
    with open(envrc_path, "r") as f:
        content = f.read()

    # Check if LOCALE_ARCHIVE is already set
    if "LOCALE_ARCHIVE" in content:
        print("LOCALE_ARCHIVE already set in .envrc")
        return False

    # Add LOCALE_ARCHIVE to .envrc
    with open(envrc_path, "a") as f:
        f.write(f"\n# Fix locale issues\nexport LOCALE_ARCHIVE=\"{locale_archive_path}\"\n")
    
    return True


def update_shell_profile(locale_archive_path):
    """Update shell profile with locale settings"""
    profile_paths = [
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
        Path.home() / ".profile"
    ]
    
    for profile_path in profile_paths:
        if profile_path.exists():
            with open(profile_path, "r") as f:
                content = f.read()
            
            # Check if LOCALE_ARCHIVE is already set
            if "LOCALE_ARCHIVE" in content:
                print(f"LOCALE_ARCHIVE already set in {profile_path}")
                continue
            
            # Add LOCALE_ARCHIVE to profile
            with open(profile_path, "a") as f:
                f.write(f"\n# Fix Nix locale issues\nexport LOCALE_ARCHIVE=\"{locale_archive_path}\"\n")
            
            print(f"Updated {profile_path}")


def main():
    """Main function"""
    # Find glibc-locales path
    locale_archive_path = find_glibc_locales()
    if not locale_archive_path:
        print("Error: Could not find glibc-locales in Nix store")
        print("Please run: nix-env -i glibc-locales")
        return 1
    
    # Update current environment
    os.environ["LOCALE_ARCHIVE"] = locale_archive_path
    print(f"Set LOCALE_ARCHIVE to {locale_archive_path}")
    
    # Update .envrc if it exists
    envrc_path = Path(".envrc")
    if envrc_path.exists():
        if update_envrc(envrc_path, locale_archive_path):
            print("Updated .envrc, run 'direnv allow' to apply changes")
    
    # Update shell profile
    update_shell_profile(locale_archive_path)
    
    print("\nLocale configuration completed.")
    print("Please restart your shell or run 'source ~/.bashrc' (or equivalent) to apply changes.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
