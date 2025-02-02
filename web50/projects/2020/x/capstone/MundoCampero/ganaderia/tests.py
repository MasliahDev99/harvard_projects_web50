from django.test import TestCase
from .models import Oveja, Venta, User, Raza, CalificadorPureza
from datetime import date

class BaseTestCase(TestCase):
    def setUp(self):
        # Create a default establishment
        self.user = User.objects.create(username='testUser', RUT=222222222222, ARU_bred_registration=124, password='Test2025@')

        # Create related objects for foreign keys, checking for existence
        raza_merino, _ = Raza.objects.get_or_create(name='Merino')
        raza_suffolk, _ = Raza.objects.get_or_create(name='Suffolk')
        raza_texel, _ = Raza.objects.get_or_create(name='Texel')
        purity_pedigree, _ = CalificadorPureza.objects.get_or_create(name='Pedigree')
        purity_po, _ = CalificadorPureza.objects.get_or_create(name='PO')
        purity_mo, _ = CalificadorPureza.objects.get_or_create(name='MO')

        # Create several sheep for testing
        self.sheep1 = Oveja.objects.create(RP='001', BU='100', sex='Male', raza=raza_merino, purity_qualifier=purity_pedigree, weight=70, establishment=self.user, birth_date='2023-01-01', age=12, name='SheePe1')
        print(f"Created sheep: {self.sheep1.name}")
        self.sheep2 = Oveja.objects.create(RP='002', BU='101', sex='Female', raza=raza_suffolk, purity_qualifier=purity_pedigree, weight=65, establishment=self.user, birth_date='2023-02-01', age=10, name='SheepPe2')
        print(f"Created sheep: {self.sheep2.name}")
        self.sheep3 = Oveja.objects.create(BU='102', sex='Male', raza=raza_texel, purity_qualifier=purity_po, weight=80, establishment=self.user, birth_date='2023-03-01', age=8, name='SheepPO1')
        print(f"Created sheep: {self.sheep3.name}")
        self.sheep4 = Oveja.objects.create(BU='103', sex='Male', raza=raza_texel, purity_qualifier=purity_mo, weight=80, establishment=self.user, birth_date='2023-03-01', age=6, name='SheepMO1')
        print(f"Created sheep: {self.sheep4.name}")

class SheepTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()  # Call the setup of BaseTestCase
        # Additional setup for sheep tests if needed

class SalesSheepTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()  # Call the setup of BaseTestCase

        # Create sales for testing
        self.auction_sale = Venta.objects.create(sale_date=date.today(), total_value=1000, establishment=self.user, sale_type='auction')
        self.auction_sale.sheep.add(self.sheep1, self.sheep2)
        print(f"Created auction sale with sheep: {[sheep.name for sheep in self.auction_sale.sheep.all()]}")

        self.individual_sale = Venta.objects.create(sale_date=date.today(), total_value=500, establishment=self.user, sale_type='individual')
        self.individual_sale.sheep.add(self.sheep1)
        print(f"Created individual sale with sheep: {[sheep.name for sheep in self.individual_sale.sheep.all()]}")

        self.slaughterhouse_sale = Venta.objects.create(sale_date=date.today(), total_value=1500, meat_value=1200, establishment=self.user, sale_type='slaughterhouse')
        self.slaughterhouse_sale.sheep.add(self.sheep2)
        print(f"Created slaughterhouse sale with sheep: {[sheep.name for sheep in self.slaughterhouse_sale.sheep.all()]}")

        self.donation_sale = Venta.objects.create(sale_date=date.today(), total_value=0, establishment=self.user, sale_type='donation')
        self.donation_sale.sheep.add(self.sheep1, self.sheep2)
        print(f"Created donation sale with sheep: {[sheep.name for sheep in self.donation_sale.sheep.all()]}")

    def test_auction_sale(self):
        """Test auction sale type."""
        self.assertEqual(self.auction_sale.sale_type, 'auction')
        self.assertEqual(self.auction_sale.sheep.count(), 2)

    def test_individual_sale(self):
        """Test individual sale type."""
        self.assertEqual(self.individual_sale.sale_type, 'individual')
        self.assertEqual(self.individual_sale.sheep.count(), 1)

    def test_slaughterhouse_sale(self):
        """Test slaughterhouse sale type."""
        self.assertEqual(self.slaughterhouse_sale.sale_type, 'slaughterhouse')
        self.assertEqual(self.slaughterhouse_sale.meat_value, 1200)

    def test_donation_sale(self):
        """Test donation sale type."""
        self.assertEqual(self.donation_sale.sale_type, 'donation')
        self.assertEqual(self.donation_sale.total_value, 0)