# Contributing to Fork Doctor

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Add tests for your changes
4. Run `pytest tests/` to verify
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push and open a Pull Request

## Development Setup

```bash
pip install -e ".[dev]"
pytest tests/
```

## Code Style
- Python 3.9+
- Use type hints
- Follow PEP 8 (max line length: 100)
- Add Jinja2 templates for new checks

## Adding a New Check
1. Add check name to `analyzer.py` CHECKS dict
2. Create template in `templates/`
3. Add template to `improver.py`
4. Add test in `tests/test_templates.py`
5. Run `fork-doctor report` on a known repo to verify

## License
MIT
