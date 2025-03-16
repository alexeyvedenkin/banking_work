from src.views import complete_result, transactions_by_period


# Тест функции transactions_by_period
def test_transactions_by_period(test_data):
    result = transactions_by_period(test_data, '01.01.2022 00:00:00')
    assert 'expenses' in result
    assert 'income' in result

# Тест функции complete_result
def test_complete_result(test_data):
    result = complete_result(test_data, '01.01.2022 00:00:00')
    assert 'expenses' in result
    assert 'income' in result
    assert 'currency_rates' in result
    assert 'stock_prices' in result

