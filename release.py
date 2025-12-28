#!/usr/bin/env python3
"""
Release Management Script for PDF OCR Processor
Helps create new releases with proper versioning and changelog updates
"""

import sys
import re
from pathlib import Path
from datetime import datetime

def get_current_version():
    """Get current version from VERSION file."""
    version_file = Path("VERSION")
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"

def parse_version(version_str):
    """Parse version string into major, minor, patch components."""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    return tuple(map(int, match.groups()))

def increment_version(current_version, bump_type):
    """Increment version based on bump type (major, minor, patch)."""
    major, minor, patch = parse_version(current_version)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

def update_version_file(new_version):
    """Update VERSION file with new version."""
    version_file = Path("VERSION")
    version_file.write_text(new_version)
    print(f"✅ Updated VERSION file to {new_version}")

def update_readme_version(new_version):
    """Update version in README.md."""
    readme_file = Path("README.md")
    if not readme_file.exists():
        print("⚠️  README.md not found, skipping version update")
        return
    
    content = readme_file.read_text()
    
    # Update version badge
    pattern = r'\*\*Version \d+\.\d+\.\d+\*\*'
    replacement = f"**Version {new_version}**"
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        readme_file.write_text(content)
        print(f"✅ Updated README.md version to {new_version}")
    else:
        print("⚠️  Version pattern not found in README.md")

def update_changelog(new_version, release_notes=None):
    """Update CHANGELOG.md with new version."""
    changelog_file = Path("CHANGELOG.md")
    if not changelog_file.exists():
        print("⚠️  CHANGELOG.md not found, skipping changelog update")
        return
    
    content = changelog_file.read_text()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find the [Unreleased] section
    unreleased_pattern = r'## \[Unreleased\]'
    
    if re.search(unreleased_pattern, content):
        # Create new version section
        new_section = f"""## [Unreleased]

### Planned
- Future enhancements and features

## [{new_version}] - {today}"""
        
        if release_notes:
            new_section += f"\n\n{release_notes}"
        
        # Replace [Unreleased] with new version section
        content = re.sub(unreleased_pattern, new_section, content)
        
        changelog_file.write_text(content)
        print(f"✅ Updated CHANGELOG.md with version {new_version}")
    else:
        print("⚠️  [Unreleased] section not found in CHANGELOG.md")

def create_git_tag(version):
    """Create git tag for the release."""
    import subprocess
    
    try:
        # Create annotated tag
        subprocess.run([
            'git', 'tag', '-a', f'v{version}', 
            '-m', f'Release version {version}'
        ], check=True)
        
        print(f"✅ Created git tag v{version}")
        print("💡 Push tag with: git push origin v{version}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create git tag: {e}")
    except FileNotFoundError:
        print("⚠️  Git not found, skipping tag creation")

def validate_release():
    """Validate that the project is ready for release."""
    issues = []
    
    # Check required files exist
    required_files = [
        'README.md', 'CHANGELOG.md', 'VERSION',
        'image_combinor/combine_recipe_pdfs.ps1',
        'aws_processor/kraken_alternative_aws.py',
        'local_processor/process_recipes_kraken_python_only.py'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            issues.append(f"Missing required file: {file_path}")
    
    # Check git status (if git is available)
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            issues.append("Uncommitted changes in git repository")
    except:
        pass  # Git not available or not a git repo
    
    return issues

def main():
    """Main release function."""
    if len(sys.argv) < 2:
        print("Usage: python release.py <major|minor|patch> [release_notes]")
        print("\nExamples:")
        print("  python release.py patch")
        print("  python release.py minor")
        print("  python release.py major")
        print('  python release.py patch "Bug fixes and improvements"')
        sys.exit(1)
    
    bump_type = sys.argv[1].lower()
    release_notes = sys.argv[2] if len(sys.argv) > 2 else None
    
    if bump_type not in ['major', 'minor', 'patch']:
        print("❌ Invalid bump type. Use: major, minor, or patch")
        sys.exit(1)
    
    print("🚀 PDF OCR Processor Release Manager")
    print("=" * 50)
    
    # Validate release readiness
    print("🔍 Validating release readiness...")
    issues = validate_release()
    if issues:
        print("❌ Release validation failed:")
        for issue in issues:
            print(f"   • {issue}")
        print("\nFix these issues before creating a release.")
        sys.exit(1)
    
    # Get current and new versions
    current_version = get_current_version()
    new_version = increment_version(current_version, bump_type)
    
    print(f"📊 Current version: {current_version}")
    print(f"📈 New version: {new_version}")
    print(f"🔄 Bump type: {bump_type}")
    
    if release_notes:
        print(f"📝 Release notes: {release_notes}")
    
    # Confirm release
    confirm = input(f"\n❓ Create release {new_version}? (y/N): ").lower().strip()
    if confirm != 'y':
        print("❌ Release cancelled")
        sys.exit(0)
    
    print(f"\n🔧 Creating release {new_version}...")
    
    # Update files
    update_version_file(new_version)
    update_readme_version(new_version)
    update_changelog(new_version, release_notes)
    
    # Create git tag
    create_git_tag(new_version)
    
    print(f"\n🎉 Release {new_version} created successfully!")
    print("\n📋 Next steps:")
    print("1. Review the updated files")
    print("2. Commit changes: git add . && git commit -m 'Release v{new_version}'")
    print("3. Push changes: git push")
    print("4. Push tag: git push origin v{new_version}")
    print("5. Create GitHub release (if using GitHub)")

if __name__ == "__main__":
    main()