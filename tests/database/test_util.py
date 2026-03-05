from __future__ import annotations

import pytest
from mikeplus import Database
from mikeplus.utilities.spatial_analysis_util import SpatialAnalysisUtil


def test_get_nearest_river_chainage_at(river_junction_couple_db):
    muid = "Node_33"
    db = Database(river_junction_couple_db)
    field_val_get = (
        db._tables.msm_Node.select(["GeomX", "GeomY"]).by_muid(muid).execute()
    )
    x = field_val_get[muid][0]
    y = field_val_get[muid][1]

    river_chainage = SpatialAnalysisUtil.get_nearest_river_chainage_at(db, x, y, 100.0)
    river = river_chainage[0]
    chainage = river_chainage[1]
    assert river == "River"
    assert chainage == pytest.approx(755.035988, abs=1e-6)
