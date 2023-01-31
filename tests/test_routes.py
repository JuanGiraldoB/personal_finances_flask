from project.models import User


class TestRoutes:
    def test_index(self, client):
        response = client.get("/")
        
        assert response.status_code == 200
        assert b"Personal Finances" in response.data 

    def test_registration(self, client, app):
        data = {
            "name": "testing",
            "email": "testing@testing.com",
            "password": "testing105369845/",
            "verify_password": "testing105369845/"
        }

        response = client.post("/register/", data=data)

        assert response.status_code == 302

        with app.app_context():
            assert User.query.count() == 1
            assert User.query.first().email == data["email"]

