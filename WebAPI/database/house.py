from ..database.base import BaseDB
from ..models.house import House, CityArea, HouseImage, Facility


class CityAreaDB(BaseDB):

    def __init__(self):
        super(CityAreaDB, self).__init__(CityArea)


class HouseDB(BaseDB):

    def __init__(self):
        super(HouseDB, self).__init__(House)


class HouseImageDB(BaseDB):

    def __init__(self):
        super(HouseImageDB, self).__init__(HouseImage)


class FacilityDB(BaseDB):

    def __init__(self):
        super(FacilityDB, self).__init__(Facility)
