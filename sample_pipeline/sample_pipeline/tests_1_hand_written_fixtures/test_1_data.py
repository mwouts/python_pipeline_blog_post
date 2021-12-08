import pandas as pd

from sample_pipeline.data import get_closes, get_volumes, get_yahoo_data


def test_get_yahoo_data(tickers, start_date, end_date):
    yahoo_data = get_yahoo_data(tickers, start_date, end_date)

    assert set(yahoo_data) == tickers
    for ticker, ticker_data in yahoo_data.items():
        assert isinstance(ticker_data, pd.DataFrame)
        assert {"Open", "High", "Low", "Close"} <= set(ticker_data.columns)
        assert "Volume" in ticker_data.columns


def assert_expected_shape(df, tickers, start_date, end_date):
    assert list(df.columns) == sorted(tickers)
    assert df.index.min() == pd.Timestamp(start_date)
    assert df.index.max() == pd.Timestamp(end_date)


def test_get_closes(yahoo_data, tickers, start_date, end_date):
    """Test that the prices look fine on a small subset"""
    closes = get_closes(yahoo_data)

    assert_expected_shape(closes, tickers, start_date, end_date)
    assert not closes.isnull().any().any()
    assert (closes > 0).all().all()


def test_get_volumes(yahoo_data, tickers, start_date, end_date):
    """Test that the volumes look fine on a small subset"""
    volumes = get_volumes(yahoo_data)

    assert_expected_shape(volumes, tickers, start_date, end_date)
    assert not volumes.isnull().any().any()
    assert (volumes > 0).all().all()
