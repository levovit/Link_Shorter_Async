import pathlib

from aiohttp.client_reqrep import ClientResponse
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from app.app import create_app
from app.settings import load_config

BASE_DIR = pathlib.Path(__file__).parent


class MyAppTestCase(AioHTTPTestCase):
    test_valid_url = "test.aiohttp/test"
    test_invalid_url = "test"

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        with open(BASE_DIR / "tests.yaml") as f:
            app = create_app(config=load_config(f))

        return await app

    # the unittest_run_loop decorator can be used in tandem with
    # the AioHTTPTestCase to simplify running
    # tests that are asynchronous
    @unittest_run_loop
    async def test_api_raw(self):
        resp: ClientResponse = await self.client.request("GET", "/api")
        json = await resp.json()
        assert resp.status == 404
        assert "error" in json
        assert json["error"]["code"] == 404
        assert json["error"]["message"] == "no links entered"

    @unittest_run_loop
    async def test_api_1_url(self):
        resp: ClientResponse = await self.client.request("GET", f'/api?url="{self.test_valid_url}"')
        json = await resp.json()
        assert resp.status == 200
        assert json["code"] == 200
        assert json["message"] == "You enter 1 links and 1 of them is valid"

    @unittest_run_loop
    async def test_api_1_url_days(self):
        resp: ClientResponse = await self.client.request("GET", f'/api?url="{self.test_valid_url}"&days=20')
        json = await resp.json()
        assert resp.status == 200
        assert json["code"] == 200
        assert json["message"] == "You enter 1 links and 1 of them is valid"

    @unittest_run_loop
    async def test_api_1_url_error(self):
        resp: ClientResponse = await self.client.request("GET", f'/api?url="{self.test_invalid_url}"')
        json = await resp.json()
        assert resp.status == 400
        assert json["code"] == 400
        assert json["message"] == "Invalid URL"

    @unittest_run_loop
    async def test_api_1_url_days_invalid(self):
        resp: ClientResponse = await self.client.request("GET", f'/api?url="{self.test_valid_url}"&days=20.2')
        json = await resp.json()
        assert resp.status == 400
        assert "error" in json
        assert json["error"]["code"] == 400
        assert json["error"]["message"] == "Invalid days number. Must be Integer"

    @unittest_run_loop
    async def test_api_1_url_days_out_of_range(self):
        resp: ClientResponse = await self.client.request("GET", f'/api?url="{self.test_valid_url}"&days=0')
        json = await resp.json()
        assert resp.status == 400
        assert "error" in json
        assert json["error"]["code"] == 400
        assert json["error"]["message"] == "Expiration date must be more than 1 day and less then year"

    @unittest_run_loop
    async def test_api_3_url(self):
        url = f'api?url1={self.test_valid_url}"&url2="{self.test_valid_url}"&url3="{self.test_valid_url}"'
        resp: ClientResponse = await self.client.request("GET", url)
        json = await resp.json()
        assert resp.status == 200
        assert json["code"] == 200
        assert json["message"] == "You enter 3 links and 3 of them is valid"

    @unittest_run_loop
    async def test_api_3_url_days(self):
        url = f'api?url1={self.test_valid_url}"&url2="{self.test_valid_url}"&url3="{self.test_valid_url}"&days=20'
        resp: ClientResponse = await self.client.request("GET", url)
        json = await resp.json()
        assert resp.status == 200
        assert json["code"] == 200
        assert json["message"] == "You enter 3 links and 3 of them is valid"

    @unittest_run_loop
    async def test_api_3_url_1_error(self):
        url = f'api?url1={self.test_valid_url}"&url2="{self.test_valid_url}"&url3="{self.test_invalid_url}"'
        resp: ClientResponse = await self.client.request("GET", url)
        json = await resp.json()
        assert resp.status == 200
        assert json["code"] == 200
        assert json["message"] == "You enter 3 links and 2 of them is valid"

    @unittest_run_loop
    async def test_api_3_url_2_error(self):
        url = f'api?url1={self.test_valid_url}"&url2="{self.test_invalid_url}"&url3="{self.test_invalid_url}"'
        resp: ClientResponse = await self.client.request("GET", url)
        json = await resp.json()
        assert resp.status == 200
        assert json["code"] == 200
        assert json["message"] == "You enter 3 links and 1 of them is valid"

    @unittest_run_loop
    async def test_api_3_url_3_error(self):
        url = f'api?url1={self.test_invalid_url}"&url2="{self.test_invalid_url}"&url3="{self.test_invalid_url}"'
        resp: ClientResponse = await self.client.request("GET", url)
        json = await resp.json()
        assert resp.status == 400
        assert json["code"] == 400
        assert json["message"] == "Invalid URL"

    @unittest_run_loop
    async def test_api_3_url_days_invalid(self):
        resp: ClientResponse = await self.client.request("GET", '/api?url="www.goo$gle.com.ua"&days=20.2')
        json = await resp.json()
        assert resp.status == 400
        assert "error" in json
        assert json["error"]["code"] == 400
        assert json["error"]["message"] == "Invalid days number. Must be Integer"

    @unittest_run_loop
    async def test_api_3_url_days_out_of_range(self):
        resp: ClientResponse = await self.client.request("GET", '/api?url="www.goo$gle.com.ua"&days=0')
        json = await resp.json()
        assert resp.status == 400
        assert "error" in json
        assert json["error"]["code"] == 400
        assert json["error"]["message"] == "Expiration date must be more than 1 day and less then year"
