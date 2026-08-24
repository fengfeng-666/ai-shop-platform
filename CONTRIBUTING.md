# Contributing to AI Shop Platform

Thank you for your interest in contributing to our AI-powered e-commerce platform!

## Getting Started

1. **Fork the repository**
2. **Clone your fork** and create a feature branch
3. **Set up your development environment** (see [README.md](README.md))

## Making Changes

### Backend Changes
- Work in the `backend/` directory
- Follow PEP 8 style guide
- Add tests for new features
- Update requirements.txt if adding dependencies

### Frontend Changes
- Work in the `frontend/` directory
- Use TypeScript and Vue 3 Composition API
- Follow existing component patterns
- Test changes in browser

### Database Changes
- Use Alembic migrations
- Create migrations for schema changes
- Test migrations thoroughly

## Submitting a Pull Request

1. Ensure your code follows the style guide
2. Update documentation as needed
3. Write a clear PR description explaining the changes
4. Reference any related issues
5. Wait for code review and address feedback

## Code Style

**Python:**
```bash
# Follow PEP 8
black .
flake8 .
```

**TypeScript/Vue:**
```bash
cd frontend
npm run lint
npm run format
```

## Testing

```bash
# Backend
cd backend
pytest --cov=app

# Frontend
cd frontend
npm run test
```

## Reporting Bugs

- Check if the bug is already reported
- Provide a clear, descriptive title
- Include steps to reproduce
- Describe the expected vs actual behavior
- Include screenshots/logs if applicable

## Suggesting Features

- Clearly describe the feature and its benefits
- Provide use cases and examples
- Consider backward compatibility
- Open an issue for discussion before starting work

## Questions?

- Open an issue with the question label
- Join our discussions for community support

---

**Thank you for making this project better!** ❤️
