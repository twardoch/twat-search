#!/bin/bash
# this_file: scripts/release.sh
# Release script for twat-search
# This script handles version management and release preparation

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Print colored output
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in a git repository
check_git() {
    if ! git rev-parse --is-inside-work-tree &> /dev/null; then
        print_error "Not in a git repository"
        exit 1
    fi
}

# Check if working directory is clean
check_clean_working_dir() {
    if [[ -n "$(git status --porcelain)" ]]; then
        print_error "Working directory is not clean. Please commit or stash changes."
        git status --short
        exit 1
    fi
    print_success "Working directory is clean"
}

# Check if we're on main branch
check_main_branch() {
    local current_branch
    current_branch="$(git branch --show-current)"
    
    if [[ "$current_branch" != "main" ]]; then
        print_error "Not on main branch (currently on: $current_branch)"
        exit 1
    fi
    print_success "On main branch"
}

# Update from remote
update_from_remote() {
    print_step "Updating from remote..."
    
    git fetch origin
    
    local local_commit remote_commit
    local_commit="$(git rev-parse HEAD)"
    remote_commit="$(git rev-parse origin/main)"
    
    if [[ "$local_commit" != "$remote_commit" ]]; then
        print_error "Local branch is not up to date with remote"
        echo "Local:  $local_commit"
        echo "Remote: $remote_commit"
        echo "Please run: git pull origin main"
        exit 1
    fi
    
    print_success "Local branch is up to date"
}

# Validate semantic version format
validate_semver() {
    local version="$1"
    
    # Remove 'v' prefix if present
    version="${version#v}"
    
    # Check if version matches semantic versioning pattern
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?(\+[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$ ]]; then
        print_error "Invalid semantic version format: $version"
        echo "Expected format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]"
        echo "Examples: 1.0.0, 1.0.0-alpha.1, 1.0.0+build.1"
        exit 1
    fi
    
    print_success "Valid semantic version: $version"
}

# Get current version from git tags
get_current_version() {
    local version
    version="$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")"
    echo "${version#v}"
}

# Get next version suggestion
suggest_next_version() {
    local current_version="$1"
    local version_type="$2"
    
    IFS='.' read -r major minor patch <<< "$current_version"
    
    case "$version_type" in
        major)
            echo "$((major + 1)).0.0"
            ;;
        minor)
            echo "$major.$((minor + 1)).0"
            ;;
        patch)
            echo "$major.$minor.$((patch + 1))"
            ;;
        *)
            echo "$current_version"
            ;;
    esac
}

# Check if tag already exists
check_tag_exists() {
    local tag="$1"
    
    if git tag -l | grep -q "^$tag$"; then
        print_error "Tag $tag already exists"
        exit 1
    fi
    
    print_success "Tag $tag is available"
}

# Run full test suite
run_tests() {
    print_step "Running full test suite..."
    
    if [[ -x "./scripts/test.sh" ]]; then
        ./scripts/test.sh --all
    else
        print_warning "Test script not found, running basic tests"
        if [[ -f ".venv/bin/activate" ]]; then
            source .venv/bin/activate
        fi
        python -m pytest tests/ -v
    fi
    
    print_success "All tests passed"
}

# Run build
run_build() {
    print_step "Running build..."
    
    if [[ -x "./scripts/build.sh" ]]; then
        ./scripts/build.sh --build
    else
        print_warning "Build script not found, running basic build"
        if [[ -f ".venv/bin/activate" ]]; then
            source .venv/bin/activate
        fi
        python -m build
    fi
    
    print_success "Build completed"
}

# Update changelog
update_changelog() {
    local version="$1"
    local changelog_file="CHANGELOG.md"
    
    print_step "Updating changelog..."
    
    if [[ ! -f "$changelog_file" ]]; then
        print_warning "Changelog file not found, creating one"
        cat > "$changelog_file" << EOF
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [$version] - $(date +%Y-%m-%d)

### Added
- Initial release

EOF
    else
        # Update existing changelog
        if grep -q "## \[Unreleased\]" "$changelog_file"; then
            # Replace [Unreleased] with version and date
            sed -i.bak "s/## \[Unreleased\]/## [$version] - $(date +%Y-%m-%d)/" "$changelog_file"
            
            # Add new [Unreleased] section at the top
            awk '/^## \[/ && !inserted {print "## [Unreleased]\n"; inserted=1} {print}' "$changelog_file" > "$changelog_file.tmp"
            mv "$changelog_file.tmp" "$changelog_file"
            
            rm -f "$changelog_file.bak"
        else
            print_warning "No [Unreleased] section found in changelog"
        fi
    fi
    
    print_success "Changelog updated"
}

# Create git tag
create_tag() {
    local version="$1"
    local tag="v$version"
    
    print_step "Creating git tag: $tag"
    
    # Create annotated tag
    git tag -a "$tag" -m "Release $version"
    
    print_success "Tag $tag created"
}

# Push to remote
push_to_remote() {
    local version="$1"
    local tag="v$version"
    local push_tags="${PUSH_TAGS:-false}"
    
    print_step "Pushing changes to remote..."
    
    # Commit changelog changes if any
    if [[ -n "$(git status --porcelain CHANGELOG.md)" ]]; then
        git add CHANGELOG.md
        git commit -m "docs: update changelog for $version"
    fi
    
    # Push main branch
    git push origin main
    
    # Push tags if requested
    if [[ "$push_tags" == "true" ]]; then
        git push origin "$tag"
        print_success "Tag $tag pushed to remote"
    else
        print_warning "Tag not pushed. Use --push-tags to push tags automatically"
        echo "To push manually: git push origin $tag"
    fi
}

# Create GitHub release
create_github_release() {
    local version="$1"
    local tag="v$version"
    
    print_step "Creating GitHub release..."
    
    if command -v gh &> /dev/null; then
        # Use GitHub CLI to create release
        gh release create "$tag" --title "Release $version" --generate-notes
        print_success "GitHub release created"
    else
        print_warning "GitHub CLI not found, skipping release creation"
        echo "To create release manually:"
        echo "  1. Go to https://github.com/your-repo/releases/new"
        echo "  2. Choose tag: $tag"
        echo "  3. Set title: Release $version"
        echo "  4. Generate release notes"
    fi
}

# Show help
show_help() {
    echo "Usage: $0 [OPTIONS] [VERSION]"
    echo ""
    echo "Release script for twat-search"
    echo ""
    echo "Arguments:"
    echo "  VERSION            Version to release (e.g., 1.0.0, 1.0.0-alpha.1)"
    echo ""
    echo "Options:"
    echo "  -h, --help         Show this help message"
    echo "  -n, --dry-run      Show what would be done without making changes"
    echo "  -f, --force        Skip some safety checks"
    echo "  -s, --skip-tests   Skip running tests"
    echo "  -b, --skip-build   Skip building package"
    echo "  -t, --push-tags    Push tags to remote automatically"
    echo "  -g, --github       Create GitHub release"
    echo "  -M, --major        Suggest next major version"
    echo "  -m, --minor        Suggest next minor version"
    echo "  -p, --patch        Suggest next patch version"
    echo "  -c, --current      Show current version"
    echo ""
    echo "Examples:"
    echo "  $0 1.0.0           # Release version 1.0.0"
    echo "  $0 --major         # Show next major version"
    echo "  $0 --minor         # Show next minor version"
    echo "  $0 --patch         # Show next patch version"
    echo "  $0 --current       # Show current version"
    echo "  $0 --dry-run 1.0.0 # Preview release without making changes"
}

# Main execution
main() {
    local version=""
    local dry_run=false
    local force=false
    local skip_tests=false
    local skip_build=false
    local show_current=false
    local suggest_major=false
    local suggest_minor=false
    local suggest_patch=false
    local create_gh_release=false
    
    export PUSH_TAGS=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -n|--dry-run)
                dry_run=true
                shift
                ;;
            -f|--force)
                force=true
                shift
                ;;
            -s|--skip-tests)
                skip_tests=true
                shift
                ;;
            -b|--skip-build)
                skip_build=true
                shift
                ;;
            -t|--push-tags)
                export PUSH_TAGS=true
                shift
                ;;
            -g|--github)
                create_gh_release=true
                shift
                ;;
            -M|--major)
                suggest_major=true
                shift
                ;;
            -m|--minor)
                suggest_minor=true
                shift
                ;;
            -p|--patch)
                suggest_patch=true
                shift
                ;;
            -c|--current)
                show_current=true
                shift
                ;;
            -*)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                version="$1"
                shift
                ;;
        esac
    done
    
    # Check prerequisites
    check_git
    
    # Handle version queries
    local current_version
    current_version="$(get_current_version)"
    
    if [[ "$show_current" == true ]]; then
        echo "$current_version"
        exit 0
    fi
    
    if [[ "$suggest_major" == true ]]; then
        suggest_next_version "$current_version" "major"
        exit 0
    fi
    
    if [[ "$suggest_minor" == true ]]; then
        suggest_next_version "$current_version" "minor"
        exit 0
    fi
    
    if [[ "$suggest_patch" == true ]]; then
        suggest_next_version "$current_version" "patch"
        exit 0
    fi
    
    # Require version if not in query mode
    if [[ -z "$version" ]]; then
        print_error "Version is required"
        echo "Current version: $current_version"
        echo "Suggestions:"
        echo "  Major: $(suggest_next_version "$current_version" "major")"
        echo "  Minor: $(suggest_next_version "$current_version" "minor")"
        echo "  Patch: $(suggest_next_version "$current_version" "patch")"
        exit 1
    fi
    
    # Remove 'v' prefix if present
    version="${version#v}"
    
    # Validate version format
    validate_semver "$version"
    
    # Check if this is a valid release
    if [[ "$force" == false ]]; then
        check_clean_working_dir
        check_main_branch
        update_from_remote
        check_tag_exists "v$version"
    fi
    
    # Show what will be done
    print_step "Preparing release $version"
    echo "Current version: $current_version"
    echo "New version: $version"
    echo "Tag: v$version"
    
    if [[ "$dry_run" == true ]]; then
        print_warning "DRY RUN - No changes will be made"
        echo "Would perform:"
        echo "  1. Update changelog"
        echo "  2. Run tests (skip: $skip_tests)"
        echo "  3. Build package (skip: $skip_build)"
        echo "  4. Create tag v$version"
        echo "  5. Push to remote (push tags: $PUSH_TAGS)"
        if [[ "$create_gh_release" == true ]]; then
            echo "  6. Create GitHub release"
        fi
        exit 0
    fi
    
    # Confirm release
    echo ""
    read -p "Proceed with release? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Release cancelled"
        exit 0
    fi
    
    # Execute release pipeline
    update_changelog "$version"
    
    if [[ "$skip_tests" == false ]]; then
        run_tests
    fi
    
    if [[ "$skip_build" == false ]]; then
        run_build
    fi
    
    create_tag "$version"
    push_to_remote "$version"
    
    if [[ "$create_gh_release" == true ]]; then
        create_github_release "$version"
    fi
    
    print_success "Release $version completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  - GitHub Actions will automatically publish to PyPI"
    echo "  - Monitor the release workflow at: https://github.com/your-repo/actions"
    if [[ "$PUSH_TAGS" == false ]]; then
        echo "  - Don't forget to push the tag: git push origin v$version"
    fi
}

# Run main function
main "$@"