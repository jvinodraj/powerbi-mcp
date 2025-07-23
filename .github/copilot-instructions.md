# Agent Instructions

When modifying code in this repository:

## Development Workflow Requirements

### **MANDATORY: Development-First Approach**
**🔬 CRITICAL: Always develop and test new functionality on live datasets using development files before modifying the main server code.**

**Development Process:**
1. **Create Development File:** Create a separate `.py` development file (e.g., `dev_column_descriptions.py`)
2. **Test on Live Dataset:** Develop and test functionality using real Power BI connection and live data
3. **Verify Functionality:** Ensure the solution works correctly with actual data from the test dataset
4. **Only Then Integrate:** Once proven to work, integrate the functionality into the main server files
5. **Run Full Test Suite:** After integration, run complete test validation

**Why This Matters:**
- **Prevents Breaking Changes:** Avoid introducing non-functional code to the main server
- **Real-World Testing:** Test against actual Power BI datasets, not just mocked data
- **Faster Iteration:** Debug and refine logic in isolation before complex integration
- **Confidence:** Ensure functionality works before modifying production code

**Example Development Pattern:**
```bash
# 1. Create development file
touch dev_new_feature.py

# 2. Develop and test with live data
python dev_new_feature.py

# 3. Once working, integrate into server.py
# 4. Run full test suite
pytest -v
```

## Learning and Knowledge Base Requirements

### **MANDATORY: Record All Corrections and Feedback**
**🧠 CRITICAL: Every time a user or operator corrects you, provides feedback, or teaches you something new, you MUST update these instructions to capture that knowledge.**

**Learning Process:**
1. **When corrected:** Immediately add the correction to the relevant section of these instructions
2. **When receiving feedback:** Update instructions with the new best practices or requirements
3. **When discovering new patterns:** Document them for future reference
4. **When making mistakes:** Add prevention guidelines to avoid repeating the same errors

**Knowledge Base Sections to Update:**
- **Technical Corrections:** Add to relevant technical sections (Environment Setup, Code Quality, Testing)
- **Process Improvements:** Add to workflow and validation sections
- **Domain-Specific Knowledge:** Create new sections for Power BI, ADOMD.NET, or MCP-specific learnings
- **Common Pitfalls:** Document mistakes and how to avoid them

**Example Update Format:**
```markdown
### **Learning from [Date]: [Brief Description]**
- **Issue:** What was wrong or needed improvement
- **Correction:** What the user/operator taught you
- **Application:** How to apply this knowledge in future work
```

**Why This Matters:**
- **Builds institutional knowledge** that persists across conversations
- **Prevents repeating the same mistakes** 
- **Improves accuracy and efficiency** over time
- **Creates a self-improving system** based on real user feedback

### **Learning from 2025-07-22: Always Test Integration Before Code Formatting**
- **Issue:** Attempted to run code formatting checks before verifying that new functionality actually works with integration tests
- **Correction:** User correctly pointed out that integration tests must be run first to verify functionality works in real environment before worrying about code formatting
- **Application:** Always follow the proper order: 1) Implement functionality, 2) Run unit tests first, 3) Run integration tests to verify it works in real environment, 4) Only then proceed with code formatting and quality checks
- **Critical Principle:** Real functionality verification comes before cosmetic code quality - never format code that doesn't work!

### **Learning from 2025-07-23: Critical Testing Regression Bug Prevention**
- **Issue:** Enhanced column descriptions functionality caused runtime error "sequence item 0: expected str instance, dict found" in production, but tests did not catch this critical bug
- **Root Cause Analysis:**
  1. **Data Structure Change:** Updated `schema['columns']` from list of strings to list of dictionaries with {name, description, data_type}
  2. **Incompatible Code:** `_handle_get_table_info()` still used `', '.join(schema['columns'])` expecting strings, not dicts
  3. **Test Gap:** Integration test `test_get_table_info_tool` was skipped due to table name parsing failure
  4. **No Unit Coverage:** No unit test specifically covered `_handle_get_table_info()` with enhanced column format
- **Prevention Strategy:**
  1. **MANDATORY: Add regression prevention tests** for all data structure changes
  2. **MANDATORY: Verify integration tests actually run** - never allow critical tests to be skipped
  3. **MANDATORY: Test format compatibility** when changing data structures
  4. **MANDATORY: Unit test critical user-facing methods** like `_handle_get_table_info()`
- **Application Rules:**
  1. **Before changing data formats:** Add tests that would catch incompatible usage
  2. **Never ignore skipped tests:** If integration tests skip, investigate and fix the reason
  3. **Test critical paths:** Methods called by external agents/users must have robust unit tests
  4. **Validate with real scenarios:** Use actual table names and data structures in tests

### **Learning from 2025-07-23: Test Parser Brittleness Prevention**
- **Issue:** Integration test parser expected old format `"- TableName"` but implementation changed to `"📊 **TableName**"` causing test to skip
- **Correction:** Test parsers must be robust and updated when output formats change
- **Application:** 
  1. **Update test parsers when changing output formats**
  2. **Make parsers more flexible** to handle format variations
  3. **Never allow critical tests to skip** without investigation
  4. **Test output format changes** in both unit and integration tests

### **Learning from 2025-07-23: Tests Should Never Skip Due to Implementation Problems**
- **Issue:** Tests were skipping when they couldn't parse output or find expected data, hiding real problems in code or test configuration
- **Correction:** User emphasized that tests should either pass or fail, never skip due to implementation issues
- **Root Cause:** Using `pytest.skip()` for parsing failures, missing data, or configuration problems masks real issues that should cause test failures
- **Application Rules:**
  1. **Only skip tests for missing external dependencies** (e.g., OpenAI API key, environment variables)
  2. **Never skip for parsing failures** - if parser can't parse output, the output format is wrong or parser needs fixing
  3. **Never skip for missing test data** - if test dataset doesn't have expected tables/columns, fix the test configuration
  4. **Use assert statements instead of skip** for implementation validation
  5. **Test failures should reveal problems** - don't hide them with skips
- **Examples of BAD skipping:**
  ```python
  # BAD: Hides parser/format problems
  if not table_name:
      pytest.skip("Could not extract table name")
      
  # BAD: Hides test configuration problems  
  if not data_tables:
      pytest.skip("No data tables found")
  ```
- **Examples of GOOD failure reporting:**
  ```python
  # GOOD: Reveals parser/format problems
  assert table_name is not None, f"Parser failed on format: {raw_output}"
  
  # GOOD: Reveals test configuration problems
  assert len(data_tables) > 0, "Test dataset should have data tables. Check configuration."
  ```

## Environment Consistency Requirements

This repository supports three distinct environments that must be kept consistent:

### 1. **Local Development Environment (Windows)**
- Windows with Visual Studio Code
- SSMS/ADOMD.NET libraries
- `.env` file for configuration
- Manual package installation

### 2. **Docker Environment (Linux)**
- Linux container with Python 3.11-slim
- Uses `install_dotnet_adomd.sh --system`
- Environment variables via `docker-entrypoint.sh`
- Systemwide .NET installation (`/usr/share/dotnet`)

### 3. **Copilot Agent Environment (Linux)**
- Linux container/codespace
- Uses `install_dotnet_adomd.sh --user`
- Environment variables via secrets (no .env file)
- User-local .NET installation (`$HOME/.local/dotnet`)

### **Consistency Rules:**
- **All environments must use the same `install_dotnet_adomd.sh` script** (with appropriate `--system` or `--user` flag)
- **All environments must use `pip install -r requirements.txt`** for Python dependencies
- **All environments must support the same core functionality** (MCP server, Power BI connectivity, testing)
- **When adding new dependencies:** Update `requirements.txt` and verify compatibility across all environments
- **When modifying installation scripts:** Test in Docker environment first, then update copilot-setup-steps.yml
- **Environment-specific differences are acceptable only for:**
  - Installation paths (system vs user)
  - Configuration delivery method (.env vs secrets)
  - Platform-specific workarounds

## Environment Setup
- Recreate the environment described in the `Dockerfile` (install the .NET runtime and ADOMD.NET library) so tests mimic the container as closely as possible.

## Code Quality Requirements
- **ALWAYS run code formatting checks before committing changes (GitHub Actions will fail otherwise):**
  ```bash
  # Check code formatting (GitHub Actions equivalent)
  black --check --diff src/ tests/ --line-length=120
  isort --check-only --diff src/ tests/ --profile=black
  flake8 src/ tests/ --config=.flake8
  
  # Auto-format code if checks fail
  black src/ tests/ --line-length=120
  isort src/ tests/ --profile=black
  ```

### **⚠️ CRITICAL: Code Formatting is MANDATORY**
- **GitHub Actions will FAIL if code is not properly formatted with black**
- **Always run `black --check` before committing**
- **All formatting issues must be fixed before push**

## Testing Requirements

### **CRITICAL: Full Test Suite Validation**
**🚨 MANDATORY: Before completing any task, ALL tests must pass. No exceptions.**

1. **Final Validation is REQUIRED:**
   ```bash
   # Complete test suite - ALL must pass
   pytest -v
   ```

2. **Never skip failing tests** - If tests fail, they must be fixed, not removed
   - Failing tests indicate broken functionality
   - Only remove tests with explicit approval from user/operator
   - Document reason for any test removal in commit message

3. **Test Execution Order** (layered approach):
   ```bash
   # 1. Unit tests (fast, isolated, mocked)
   pytest tests/unit/ -v
   
   # 2. Local tests (require server startup)
   pytest tests/local/ -v
   
   # 3. Integration tests (require external services)
   pytest tests/integration/ -v
   ```

### **Test Development Guidelines**
- Always run `pytest -q` after changes
- For every new or modified feature, add or update tests to cover the change
- **Maintain test isolation** - tests must not depend on each other
- **Use appropriate test markers:**
  - `@pytest.mark.unit` for unit tests
  - `@pytest.mark.local` for local server tests  
  - `@pytest.mark.integration` for integration tests

### **When Tests Fail**
1. **DO NOT COMMIT** until all tests pass
2. **DO NOT DELETE** failing tests without approval
3. **Investigate and fix** the root cause
4. If unsure about test removal, ask: "Should I remove test X because of reason Y?"

### **Code Quality Integration**
- **Run formatting checks as part of testing workflow (MANDATORY before commit):**
  ```bash
  # Full local validation (same as CI/CD pipeline)
  black --check --diff src/ tests/ --line-length=120  # ⚠️ MUST PASS - GitHub Actions requirement
  isort --check-only --diff src/ tests/ --profile=black
  flake8 src/ tests/ --config=.flake8
  
  # Run all test layers
  pytest tests/unit/ -v --tb=short
  pytest tests/local/ -v --tb=short  
  pytest tests/integration/ -v --tb=short
  ```

## Why This Matters
- **🚨 CRITICAL: GitHub Actions will fail if code is not properly formatted with black**
- **Formatting checks are part of CI/CD pipeline and will block merges**
- Consistent formatting improves code readability and maintainability
- Following these steps ensures CI/CD pipeline success

## Quick Validation Commands
```bash
# Code quality and unit tests (fast) - includes mandatory formatting checks
black --check --diff src/ tests/ --line-length=120 && isort --check-only src/ tests/ --profile=black && flake8 src/ tests/ --config=.flake8 && pytest tests/unit/ -v && echo "✅ Code quality and unit tests passed!"

# Full validation including all test layers (comprehensive)
black --check --diff src/ tests/ --line-length=120 && isort --check-only src/ tests/ --profile=black && flake8 src/ tests/ --config=.flake8 && pytest -v && echo "🎉 ALL TESTS PASSED - Ready to commit!"

# Auto-fix formatting if checks fail, then validate again
black src/ tests/ --line-length=120 && isort src/ tests/ --profile=black && echo "🔧 Formatting fixed - now run validation again"
```
