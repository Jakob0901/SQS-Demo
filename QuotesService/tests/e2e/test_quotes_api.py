import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def setup(page: Page):
    # Navigate to your app before each test
    page.goto('http://localhost:80')
    yield page


def test_initial_page_load(page: Page):
    # Check if main elements are visible
    expect(page.locator('h1')).to_contain_text('Zitate-Service')
    expect(page.locator('.btn-primary')).to_be_visible()
    expect(page.locator('.btn-success')).to_be_disabled()


def test_quote_retrieval(page: Page):
    # Click the "Neues Zitat" button
    page.click('text=Neues Zitat')
    # Verify quote card is not empty
    expect(page.locator('.card-text')).not_to_be_empty()


def test_api_key_connection(page: Page):
    # Fill in API key
    page.fill('input[type="password"]', 'test_api_key')
    # Click connect button
    page.click('text=Verbinden')
    # Verify save button is enabled
    expect(page.locator('.btn-success')).to_be_enabled()


def test_save_quote(page: Page):
    # Setup: Connect with API key
    page.fill('input[type="password"]', 'test_api_key')
    page.click('text=Verbinden')

    # Get initial quote count
    initial_quotes = page.locator('.list-group-item').count()

    # Click save button
    page.click('text=Speichern')

    # Verify new quote appears in saved quotes
    expect(page.locator('.list-group-item')).to_have_count(initial_quotes + 1)