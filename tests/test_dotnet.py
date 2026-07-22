"""Regression tests for Python-to-.NET value conversion."""

import datetime

import pytest
from mikeplus.dotnet import DotNetConverter
import System
from System.Data import DbType


@pytest.mark.parametrize("value", ["760309", "33,34"])
def test_arbitrary_strings_are_not_inferred_as_datetimes(value):
    """Keep numeric-looking identifiers and comma-separated text as strings."""
    converted = DotNetConverter.to_dotnet_value(value)

    assert isinstance(converted, str)
    assert converted == value


def test_dictionary_conversion_respects_schema_column_types():
    """Convert only strings belonging to schema-declared DateTime fields."""
    values = {
        "assetname": "760309",
        "dem_location": "33,34",
        "ComputationBegin": "2025-01-01 14:30:00",
    }
    column_types = {
        "assetname": DbType.String,
        "dem_location": DbType.String,
        "computationbegin": DbType.DateTime,
    }

    converted = DotNetConverter.to_dotnet_dictionary(values, column_types)

    assert converted["assetname"] == "760309"
    assert converted["dem_location"] == "33,34"
    assert isinstance(converted["ComputationBegin"], System.DateTime)
    assert DotNetConverter.from_dotnet_datetime(
        converted["ComputationBegin"]
    ) == datetime.datetime(2025, 1, 1, 14, 30)
