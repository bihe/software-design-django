# Project rules

- The project uses uv (https://github.com/astral-sh/uv)
- Sync dependencies `uv sync`
- Ensure the virtual environment is active `source .venv/bin/activate`

# Django rules

- Use `uv run python manage.py startapp` to create new apps within your project
- Keep models in `models.py` and register them in `admin.py` for admin interface
- Create tests for models and put them into `test_models.py`
- Use `django.test.TestCase` for testing models
- Use Django's ORM instead of raw SQL queries
- Avoid N+1 queries with `select_related` and `prefetch_related`:

```python
# Good pattern
users = User.objects.select_related('profile')
posts = Post.objects.prefetch_related('tags')
```

- Use Django forms for validation:

```python
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
```

- Create custom model managers for common queries:

```python
class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
```

- Use Django's built-in authentication system
- Store settings in environment variables and adccess via `settings.py`

- Create business logic in `services.py`
- Create tests for services in `test_services.py`
- Use python unittests `unittest.TestCase`
  