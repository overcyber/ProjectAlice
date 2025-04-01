# ProjectAlice Guidelines for Claude

## Build Commands
- Install: `pip install -r requirements.txt` and `pip install -r requirements_test.txt`
- Run tests: `pytest tests/ --cov=core/ --cov-report=xml`
- Run single test: `pytest tests/path/to/test_file.py::TestClass::test_method`
- Lint: Use SonarCloud for code quality checks

## Code Style
- **Naming**: Classes use PascalCase, methods/variables use camelCase
- **Privacy**: Prefix private members with underscore (_variable)
- **Imports**: Group by standard library, third-party, then project modules
- **Documentation**: Rich docstrings with type hints
- **Design Patterns**: Singleton pattern is used extensively 
- **Error Handling**: Use custom exceptions inherited from ProjectAliceException
- **Logging**: Use Logger consistently with appropriate severity levels

## Project Structure
- Core functionality: `/core`
- Tests: `/tests` (mirrors core structure)
- Skills: `/skills` 
- System resources: `/system`

Refer to [Project Alice documentation](https://docs.projectalice.io) for additional information.