from django.urls import reverse, resolve
from final.models import Vehicle
from datetime import datetime
import pytest
class TestUrls:

    def test_detail_login(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_detail_sign_up(self):
        path = reverse('sign_up')
        assert resolve(path).view_name == 'sign_up'

    def test_detail_home(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def test_detail_input_your_vehicle(self):
        path = reverse('input_your_vehicle')
        assert resolve(path).view_name == 'input_your_vehicle'

    def test_detail_input_your_fleet(self):
        path = reverse('input_your_fleet')
        assert resolve(path).view_name == 'input_your_fleet'


class TestModels:

    @pytest.mark.django_db
    def testmodel(self):
        vehicle = Vehicle.objects.create(
            vin='zxcvbnmasdfghjklq',
            avgFuelConsumptionPer100Km= 25.2,
            distance_traveled = 2342,
            fuel_consumed = 2423,
            last_data_upload = datetime.now(),
            first_data_upload = datetime.now(),
            average_fuel_consumption_from_update = 21.23,
            days_from_update = 2141,
        )
