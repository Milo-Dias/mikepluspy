from mikeplus.tables.base_table import BaseTable
from mikeplus.tables.base_table import BaseColumns

class mw_WDOAmiTableColumns(BaseColumns):
    """Column names for mw_WDOAmi (Advanced metering infrastructure)."""
    MUID = "MUID"
    """ID"""
    SensorID = "SensorID"
    """Sensor ID"""
    SensorTable = "SensorTable"
    """Sensor Table"""
    Mult = "Mult"
    """Multiplier [()]"""
    OffsetValue = "OffsetValue"
    """Offset"""
    Comment = "Comment"
    """Description"""
    Enabled = "Enabled"
    """Is active"""

class mw_WDOAmiTable(BaseTable):
    """Table for mw_WDOAmi (Advanced metering infrastructure)."""
    
    @property
    def columns(self) -> mw_WDOAmiTableColumns:
        """Get the columns for the table."""
        if self._columns is None:
            self._columns = mw_WDOAmiTableColumns(self)
        return self._columns