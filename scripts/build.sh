#!/bin/bash
# this_file: scripts/build.sh
# Build script for twat-search
# This script provides a comprehensive build pipeline for local development

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

# Check if uv is available
check_uv() {
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Installing..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source "$HOME/.local/bin/env"
    fi
}

# Setup virtual environment
setup_venv() {
    print_step "Setting up virtual environment..."
    
    if [[ ! -d ".venv" ]]; then
        uv venv --python 3.12
        print_success "Created virtual environment"
    else
        print_success "Virtual environment already exists"
    fi
}

# Install dependencies
install_deps() {
    print_step "Installing dependencies..."
    
    source .venv/bin/activate
    uv pip install -e ".[dev,test,all]"
    
    print_success "Dependencies installed"
}

# Run code quality checks
run_quality_checks() {
    print_step "Running code quality checks..."
    
    source .venv/bin/activate
    
    # Format code
    echo "  Formatting code with ruff..."
    if ruff format --respect-gitignore src/twat_search tests; then
        print_success "Code formatting passed"
    else
        print_error "Code formatting failed"
        return 1
    fi
    
    # Lint code
    echo "  Linting code with ruff..."
    if ruff check src/twat_search tests; then
        print_success "Linting passed"
    else
        print_error "Linting failed"
        return 1
    fi
    
    # Type checking
    echo "  Type checking with mypy..."
    if mypy src/twat_search tests; then
        print_success "Type checking passed"
    else
        print_error "Type checking failed"
        return 1
    fi
}

# Run tests
run_tests() {
    print_step "Running tests..."
    
    source .venv/bin/activate
    
    # Run tests with coverage
    if python -m pytest tests/ -v --cov=src/twat_search --cov-report=term-missing --cov-report=html --cov-report=xml; then
        print_success "Tests passed"
    else
        print_error "Tests failed"
        return 1
    fi
}

# Build package
build_package() {
    print_step "Building package..."
    
    source .venv/bin/activate
    
    # Clean previous builds
    rm -rf dist/ build/ *.egg-info/
    
    # Build package
    if python -m build; then
        print_success "Package built successfully"
        echo "  Built files:"
        ls -la dist/
    else
        print_error "Package build failed"
        return 1
    fi
}

# Validate package
validate_package() {
    print_step "Validating package..."
    
    source .venv/bin/activate
    
    # Check package with twine
    if command -v twine &> /dev/null; then
        if twine check dist/*; then
            print_success "Package validation passed"
        else
            print_error "Package validation failed"
            return 1
        fi
    else
        print_warning "twine not available, skipping package validation"
    fi
}

# Show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Build script for twat-search"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message"
    echo "  -q, --quality     Run only code quality checks"
    echo "  -t, --test        Run only tests"
    echo "  -b, --build       Run only build"
    echo "  -f, --full        Run full pipeline (default)"
    echo "  -s, --skip-tests  Skip test execution"
    echo "  -v, --verbose     Verbose output"
    echo ""
    echo "Examples:"
    echo "  $0                # Full build pipeline"
    echo "  $0 --quality      # Only code quality checks"
    echo "  $0 --test         # Only run tests"
    echo "  $0 --build        # Only build package"
    echo "  $0 --skip-tests   # Build without tests"
}

# Main execution
main() {
    local run_quality=false
    local run_test=false
    local run_build=false
    local skip_tests=false
    local verbose=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -q|--quality)
                run_quality=true
                shift
                ;;
            -t|--test)
                run_test=true
                shift
                ;;
            -b|--build)
                run_build=true
                shift
                ;;
            -f|--full)
                run_quality=true
                run_test=true
                run_build=true
                shift
                ;;
            -s|--skip-tests)
                skip_tests=true
                shift
                ;;
            -v|--verbose)
                verbose=true
                set -x
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Default to full pipeline if no specific options
    if [[ "$run_quality" == false && "$run_test" == false && "$run_build" == false ]]; then
        run_quality=true
        run_test=true
        run_build=true
    fi
    
    # Override test if skip_tests is set
    if [[ "$skip_tests" == true ]]; then
        run_test=false
    fi
    
    print_step "Starting build pipeline for twat-search"
    
    # Check prerequisites
    check_uv
    setup_venv
    install_deps
    
    # Run selected pipeline steps
    if [[ "$run_quality" == true ]]; then
        run_quality_checks || exit 1
    fi
    
    if [[ "$run_test" == true ]]; then
        run_tests || exit 1
    fi
    
    if [[ "$run_build" == true ]]; then
        build_package || exit 1
        validate_package || exit 1
    fi
    
    print_success "Build pipeline completed successfully!"
    
    if [[ "$run_build" == true ]]; then
        echo ""
        echo "Built artifacts:"
        ls -la dist/
        echo ""
        echo "To install locally: pip install dist/*.whl"
        echo "To upload to PyPI: twine upload dist/*"
    fi
}

# Run main function
main "$@"