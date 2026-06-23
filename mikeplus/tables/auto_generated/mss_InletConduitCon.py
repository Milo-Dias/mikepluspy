from mikeplus.tables.base_geometry_table import BaseGeometryTable
from mikeplus.tables.base_geometry_table import BaseColumns

class mss_InletConduitConTableColumns(BaseColumns):
    """Column names for mss_InletConduitCon (Inlets Connections)."""
    MUID = "MUID"
    """ID"""
    LinkID = "LinkID"
    """Link ID"""

class mss_InletConduitConTable(BaseGeometryTable):
    """Table for mss_InletConduitCon (Inlets Connections)."""
    
    @property
    def columns(self) -> mss_InletConduitConTableColumns:
        """Get the columns for the table."""
        if self._columns is None:
            self._columns = mss_InletConduitConTableColumns(self)
        return self._columns