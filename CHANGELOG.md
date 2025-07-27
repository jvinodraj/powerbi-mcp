# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2025-01-18

### Added
- Integration tests for real Power BI connectivity
- Environment-based integration test configuration
- Interactive test runner with safety checks
- GitHub Actions CI/CD workflow for automated testing
- Comprehensive integration test documentation
- Test markers for unit vs integration test separation
- Makefile for simplified development workflow
- Enhanced error handling and validation in tests

### Changed
- Updated .env.example with integration test configuration
- Improved test structure with proper pytest markers
- Enhanced documentation with integration testing guide

### Security
- Secure handling of test credentials via environment variables
- Clear separation of test and production configurations

## [1.0.0] - 2024-06-21

### Added
- Initial release of Power BI MCP Server
- Natural language to DAX query generation
- Service Principal authentication
- Async performance optimizations
- Comprehensive error handling
- Support for GPT-4o-mini model
- Table and schema discovery
- Custom DAX execution
- Intelligent question suggestions

### Security
- Secure credential handling via environment variables
- No hardcoded secrets in codebase
