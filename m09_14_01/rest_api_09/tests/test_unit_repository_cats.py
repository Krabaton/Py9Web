import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Cat, Owner
from src.schemas import CatModel, CatVaccinatedModel
from src.repository.cats import get_cats, get_cat_by_id, create, remove, update, set_vaccinated


class TestCatsRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.owner = Owner(id=1, email='test@test.com')

    async def test_get_cats(self):
        cats = [Cat(), Cat(), Cat()]
        self.session.query().limit().offset().all.return_value = cats
        result = await get_cats(10, 0, self.session)
        self.assertEqual(result, cats)

    async def test_create_cat(self):
        body = CatModel(
            nickname='Simon',
            age=5,
            vaccinated=True,
            description='Дуже багато мяукає',
            owner_id=self.owner.id
        )
        result = await create(body, self.session)
        print(result)
        self.assertEqual(result.nickname, body.nickname)
        self.assertTrue(hasattr(result, 'id'))
