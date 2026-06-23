from mikeplus.tables.base_table import BaseTable
from mikeplus.tables.base_table import BaseColumns

class m_GenericSettingTableColumns(BaseColumns):
    """Column names for m_GenericSetting (m_GenericSetting)."""
    MUID = "MUID"
    """ID"""
    TypeNo = "TypeNo"
    """Value int"""
    ValueInt = "ValueInt"
    """Value int"""
    ValueIntDom = "ValueIntDom"
    """Value int"""
    ValueText = "ValueText"
    """Value text"""
    ValueDt = "ValueDt"
    """Value datetime"""
    ValueFilePath = "ValueFilePath"
    """ValueFilePath"""
    ControlNo = "ControlNo"
    """ControlNo"""

class m_GenericSettingTable(BaseTable):
    """Table for m_GenericSetting (m_GenericSetting)."""
    
    @property
    def columns(self) -> m_GenericSettingTableColumns:
        """Get the columns for the table."""
        if self._columns is None:
            self._columns = m_GenericSettingTableColumns(self)
        return self._columns