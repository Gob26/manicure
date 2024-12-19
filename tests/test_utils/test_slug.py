import pytest
from unittest import mock
from slugify import slugify
from tortoise import fields
from tortoise.models import Model

from app.use_case.utils.slug_generator import generate_unique_slug


class MyModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255)

@pytest.mark.asyncio
async def test_generate_unique_slug():
    # Create mock model and query set
    mock_queryset = mock.AsyncMock()
    mock_model = mock.AsyncMock()
    
    # Configure the filter to return the queryset
    mock_model.filter.return_value = mock_queryset
    
    # First test case: slug exists once, then doesn't exist
    mock_queryset.exists.side_effect = [True, False]
    
    name = "Test Name"
    generated_slug = await generate_unique_slug(mock_model, name)
    
    expected_slug = "test-name-1"
    assert generated_slug == expected_slug, f"Expected {expected_slug}, but got {generated_slug}"
    
    # Verify filter was called with correct arguments
    mock_model.filter.assert_any_call(slug="test-name")
    mock_model.filter.assert_any_call(slug="test-name-1")
    
    # Reset mocks for second test
    mock_model.reset_mock()
    mock_queryset.reset_mock()
    
    # Second test case: slug doesn't exist on first try
    mock_queryset.exists.side_effect = [False]
    
    generated_slug_first_time = await generate_unique_slug(mock_model, name)
    expected_slug_first_time = "test-name"
    assert generated_slug_first_time == expected_slug_first_time, \
        f"Expected {expected_slug_first_time}, but got {generated_slug_first_time}"