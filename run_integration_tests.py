#!/usr/bin/env python3
"""
Test runner script for Power BI MCP Integration Tests.

This script checks if integration tests are enabled and runs them
with proper configuration.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def main():
    """Main test runner function."""
    # Load environment variables
    load_dotenv()
    
    # Check if integration tests are enabled
    integration_enabled = os.getenv("ENABLE_INTEGRATION_TESTS", "false").lower() == "true"
    
    print("Power BI MCP Integration Test Runner")
    print("=" * 40)
    
    if not integration_enabled:
        print("❌ Integration tests are DISABLED")
        print()
        print("To enable integration tests:")
        print("1. Copy .env.example to .env")
        print("2. Set ENABLE_INTEGRATION_TESTS=true")
        print("3. Configure the following variables:")
        print("   - TEST_XMLA_ENDPOINT")
        print("   - TEST_TENANT_ID")
        print("   - TEST_CLIENT_ID")
        print("   - TEST_CLIENT_SECRET")
        print("   - TEST_INITIAL_CATALOG")
        print()
        print("Optional configuration:")
        print("   - TEST_EXPECTED_TABLE")
        print("   - TEST_EXPECTED_COLUMN")
        print("   - TEST_DAX_QUERY")
        print("   - TEST_MIN_TABLES_COUNT")
        print("   - OPENAI_API_KEY (for AI features)")
        return 1
    
    print("✅ Integration tests are ENABLED")
    
    # Check if ADOMD.NET is available
    try:
        import sys as sys_module
        sys_module.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
        from server import PowerBIConnector
        connector = PowerBIConnector()
        connector._check_pyadomd()
        print("✅ ADOMD.NET library is available")
    except Exception as e:
        if "System.Configuration.ConfigurationManager" in str(e):
            print("❌ ADOMD.NET configuration issue detected:")
            print("   Missing: System.Configuration.ConfigurationManager")
            print()
            print("🔧 Solutions:")
            print("1. Use Docker (recommended):")
            print("   docker build -t powerbi-mcp .")
            print("   docker run --rm -e ENABLE_INTEGRATION_TESTS=true powerbi-mcp")
            print()
            print("2. Install missing .NET dependency:")
            print("   - Install SQL Server Management Studio")
            print("   - Or use .NET Framework version of ADOMD.NET")
            print()
            print("3. See docs/TROUBLESHOOTING_INTEGRATION.md for detailed instructions")
            return 1
        elif "pyadomd not available" in str(e):
            print("❌ PyADOMD library not available:")
            print("   This usually indicates ADOMD.NET is not properly installed")
            print()
            print("🔧 Solutions:")
            print("1. Install SQL Server Management Studio (includes ADOMD.NET)")
            print("2. Use Docker environment which includes all dependencies")
            print("3. See docs/TROUBLESHOOTING_INTEGRATION.md")
            return 1
        else:
            print(f"⚠️  ADOMD.NET check failed: {e}")
            print("   Tests may fail due to missing dependencies")
    
    # Check required configuration
    required_vars = [
        "TEST_XMLA_ENDPOINT",
        "TEST_TENANT_ID", 
        "TEST_CLIENT_ID",
        "TEST_CLIENT_SECRET",
        "TEST_INITIAL_CATALOG"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required configuration: {', '.join(missing_vars)}")
        print("Please configure these variables in your .env file")
        return 1
    
    print("✅ Required configuration found")
    
    # Check optional OpenAI configuration
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key found - AI features will be tested")
    else:
        print("⚠️  OpenAI API key not found - AI features will be skipped")
    
    print()
    print("Test Configuration:")
    print(f"  Dataset: {os.getenv('TEST_INITIAL_CATALOG')}")
    print(f"  Endpoint: {os.getenv('TEST_XMLA_ENDPOINT')}")
    print(f"  Expected Table: {os.getenv('TEST_EXPECTED_TABLE', 'Not configured')}")
    print(f"  Min Tables: {os.getenv('TEST_MIN_TABLES_COUNT', '1')}")
    
    print()
    print("⚠️  WARNING: These tests will connect to real Power BI datasets")
    print("   and may consume API quota. Continue? (y/N): ", end="")
    
    if "--yes" in sys.argv or "-y" in sys.argv:
        response = "y"
        print("y (auto-confirmed)")
    else:
        response = input().lower()
    
    if response != "y":
        print("❌ Tests cancelled by user")
        return 1
    
    print()
    print("🚀 Running integration tests...")
    print("=" * 40)
    
    # Run pytest with integration test file
    test_file = Path(__file__).parent / "tests" / "test_integration.py"
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_file),
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    # Add any additional pytest arguments
    if len(sys.argv) > 1:
        cmd.extend([arg for arg in sys.argv[1:] if arg not in ["--yes", "-y"]])
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
