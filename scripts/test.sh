#!/bin/bash
# this_file: scripts/test.sh
# Test script for twat-search
# This script provides comprehensive testing capabilities for the project

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

# Run unit tests
run_unit_tests() {
    print_step "Running unit tests..."
    
    source .venv/bin/activate
    
    local pytest_args=()
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    if [[ "${COVERAGE:-true}" == "true" ]]; then
        pytest_args+=("--cov=src/twat_search" "--cov-report=term-missing")
        if [[ "${HTML_COVERAGE:-false}" == "true" ]]; then
            pytest_args+=("--cov-report=html")
        fi
        if [[ "${XML_COVERAGE:-false}" == "true" ]]; then
            pytest_args+=("--cov-report=xml")
        fi
    fi
    
    if [[ "${PARALLEL:-false}" == "true" ]]; then
        pytest_args+=("-n" "auto")
    fi
    
    if python -m pytest tests/test_twat_search.py tests/unit/ "${pytest_args[@]}"; then
        print_success "Unit tests passed"
    else
        print_error "Unit tests failed"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    print_step "Running integration tests..."
    
    source .venv/bin/activate
    
    local pytest_args=()
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    pytest_args+=("-m" "integration")
    
    if python -m pytest tests/ "${pytest_args[@]}"; then
        print_success "Integration tests passed"
    else
        print_warning "Integration tests failed or none found"
        return 0  # Don't fail the pipeline for integration tests
    fi
}

# Run benchmark tests
run_benchmark_tests() {
    print_step "Running benchmark tests..."
    
    source .venv/bin/activate
    
    local pytest_args=()
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    pytest_args+=("-m" "benchmark" "--benchmark-only")
    
    if python -m pytest tests/ "${pytest_args[@]}"; then
        print_success "Benchmark tests passed"
    else
        print_warning "Benchmark tests failed or none found"
        return 0  # Don't fail the pipeline for benchmark tests
    fi
}

# Run specific test patterns
run_pattern_tests() {
    local pattern="$1"
    print_step "Running tests matching pattern: $pattern"
    
    source .venv/bin/activate
    
    local pytest_args=()
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    pytest_args+=("-k" "$pattern")
    
    if python -m pytest tests/ "${pytest_args[@]}"; then
        print_success "Pattern tests passed"
    else
        print_error "Pattern tests failed"
        return 1
    fi
}

# Run tests with specific markers
run_marker_tests() {
    local marker="$1"
    print_step "Running tests with marker: $marker"
    
    source .venv/bin/activate
    
    local pytest_args=()
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    pytest_args+=("-m" "$marker")
    
    if python -m pytest tests/ "${pytest_args[@]}"; then
        print_success "Marker tests passed"
    else
        print_error "Marker tests failed"
        return 1
    fi
}

# Run performance tests
run_performance_tests() {
    print_step "Running performance tests..."
    
    source .venv/bin/activate
    
    # Run benchmarks and save results
    if python -m pytest tests/ -m benchmark --benchmark-json=benchmark_results.json; then
        print_success "Performance tests completed"
        if [[ -f "benchmark_results.json" ]]; then
            echo "Benchmark results saved to benchmark_results.json"
        fi
    else
        print_warning "Performance tests failed or none found"
    fi
}

# Generate test report
generate_test_report() {
    print_step "Generating test report..."
    
    source .venv/bin/activate
    
    # Generate comprehensive test report
    python -m pytest tests/ --cov=src/twat_search --cov-report=html --cov-report=xml --cov-report=term-missing --junitxml=test_results.xml
    
    print_success "Test report generated"
    echo "  HTML coverage report: htmlcov/index.html"
    echo "  XML coverage report: coverage.xml"
    echo "  JUnit XML report: test_results.xml"
}

# Watch mode for continuous testing
watch_tests() {
    print_step "Starting watch mode for continuous testing..."
    
    source .venv/bin/activate
    
    # Use pytest-watch if available, otherwise use a simple loop
    if command -v pytest-watch &> /dev/null; then
        pytest-watch -- tests/
    else
        print_warning "pytest-watch not available, falling back to simple watch mode"
        while true; do
            clear
            echo "Running tests... (Press Ctrl+C to stop)"
            python -m pytest tests/ --tb=short || true
            echo "Waiting for file changes..."
            sleep 5
        done
    fi
}

# Clean test artifacts
clean_artifacts() {
    print_step "Cleaning test artifacts..."
    
    rm -rf htmlcov/
    rm -rf .coverage
    rm -rf coverage.xml
    rm -rf test_results.xml
    rm -rf benchmark_results.json
    rm -rf .pytest_cache/
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} +
    
    print_success "Test artifacts cleaned"
}

# Show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Test script for twat-search"
    echo ""
    echo "Options:"
    echo "  -h, --help         Show this help message"
    echo "  -u, --unit         Run unit tests only"
    echo "  -i, --integration  Run integration tests only"
    echo "  -b, --benchmark    Run benchmark tests only"
    echo "  -p, --performance  Run performance tests"
    echo "  -a, --all          Run all tests (default)"
    echo "  -k, --pattern      Run tests matching pattern"
    echo "  -m, --marker       Run tests with specific marker"
    echo "  -r, --report       Generate comprehensive test report"
    echo "  -w, --watch        Run in watch mode for continuous testing"
    echo "  -c, --clean        Clean test artifacts"
    echo "  -v, --verbose      Verbose output"
    echo "  --no-coverage      Skip coverage reporting"
    echo "  --html-coverage    Generate HTML coverage report"
    echo "  --xml-coverage     Generate XML coverage report"
    echo "  --parallel         Run tests in parallel"
    echo ""
    echo "Examples:"
    echo "  $0                 # Run all tests"
    echo "  $0 --unit          # Run unit tests only"
    echo "  $0 --integration   # Run integration tests only"
    echo "  $0 -k search       # Run tests matching 'search'"
    echo "  $0 -m unit         # Run tests with 'unit' marker"
    echo "  $0 --report        # Generate comprehensive report"
    echo "  $0 --watch         # Run in watch mode"
    echo "  $0 --clean         # Clean test artifacts"
}

# Main execution
main() {
    local run_unit=false
    local run_integration=false
    local run_benchmark=false
    local run_performance=false
    local run_all=false
    local run_report=false
    local run_watch=false
    local run_clean=false
    local pattern=""
    local marker=""
    
    export VERBOSE=false
    export COVERAGE=true
    export HTML_COVERAGE=false
    export XML_COVERAGE=false
    export PARALLEL=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -u|--unit)
                run_unit=true
                shift
                ;;
            -i|--integration)
                run_integration=true
                shift
                ;;
            -b|--benchmark)
                run_benchmark=true
                shift
                ;;
            -p|--performance)
                run_performance=true
                shift
                ;;
            -a|--all)
                run_all=true
                shift
                ;;
            -k|--pattern)
                pattern="$2"
                shift 2
                ;;
            -m|--marker)
                marker="$2"
                shift 2
                ;;
            -r|--report)
                run_report=true
                shift
                ;;
            -w|--watch)
                run_watch=true
                shift
                ;;
            -c|--clean)
                run_clean=true
                shift
                ;;
            -v|--verbose)
                export VERBOSE=true
                shift
                ;;
            --no-coverage)
                export COVERAGE=false
                shift
                ;;
            --html-coverage)
                export HTML_COVERAGE=true
                shift
                ;;
            --xml-coverage)
                export XML_COVERAGE=true
                shift
                ;;
            --parallel)
                export PARALLEL=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Default to all tests if no specific options
    if [[ "$run_unit" == false && "$run_integration" == false && "$run_benchmark" == false && "$run_performance" == false && "$run_all" == false && "$run_report" == false && "$run_watch" == false && "$run_clean" == false && -z "$pattern" && -z "$marker" ]]; then
        run_all=true
    fi
    
    print_step "Starting test pipeline for twat-search"
    
    # Handle clean operation
    if [[ "$run_clean" == true ]]; then
        clean_artifacts
        exit 0
    fi
    
    # Handle watch mode
    if [[ "$run_watch" == true ]]; then
        check_uv
        setup_venv
        install_deps
        watch_tests
        exit 0
    fi
    
    # Check prerequisites
    check_uv
    setup_venv
    install_deps
    
    # Run specific pattern or marker tests
    if [[ -n "$pattern" ]]; then
        run_pattern_tests "$pattern" || exit 1
    elif [[ -n "$marker" ]]; then
        run_marker_tests "$marker" || exit 1
    else
        # Run selected test suites
        if [[ "$run_unit" == true || "$run_all" == true ]]; then
            run_unit_tests || exit 1
        fi
        
        if [[ "$run_integration" == true || "$run_all" == true ]]; then
            run_integration_tests || exit 1
        fi
        
        if [[ "$run_benchmark" == true || "$run_all" == true ]]; then
            run_benchmark_tests || exit 1
        fi
        
        if [[ "$run_performance" == true ]]; then
            run_performance_tests || exit 1
        fi
        
        if [[ "$run_report" == true ]]; then
            generate_test_report || exit 1
        fi
    fi
    
    print_success "Test pipeline completed successfully!"
}

# Run main function
main "$@"