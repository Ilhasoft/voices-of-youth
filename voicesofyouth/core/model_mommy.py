from mommy_spatial_generators import MOMMY_SPATIAL_FIELDS
from mommy_spatial_generators.generators import gen_linestring
from mommy_spatial_generators.generators import gen_point
from mommy_spatial_generators.generators import gen_multipoint


def _gen_linestring():
    return gen_linestring(min_x=-120, min_y=-50, max_x=120, max_y=50)


def _gen_multipoint():
    return gen_multipoint(min_x=-120, min_y=-50, max_x=120, max_y=50)


def _gen_point():
    return gen_point(min_x=-120, min_y=-50, max_x=120, max_y=50)


def _gen_multilinestring():
    return gen_multilinestring(min_x=-120, min_y=-50, max_x=120, max_y=50)


MOMMY_SPATIAL_FIELDS["django.contrib.gis.db.models.PointField"] = _gen_point
MOMMY_SPATIAL_FIELDS["django.contrib.gis.db.models.MultiPointField"] = _gen_multipoint,
MOMMY_SPATIAL_FIELDS["django.contrib.gis.db.models.LineStringField"] = _gen_linestring,
MOMMY_SPATIAL_FIELDS["django.contrib.gis.db.models.MultiLineStringField"] = _gen_multilinestring,
