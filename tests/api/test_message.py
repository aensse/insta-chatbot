import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_background_tasks
from app.main import app

client = TestClient(app)


def override_background_tasks():
    class BackgroundTasksMocker:
        def add_task(self, *args):
            return True

    return BackgroundTasksMocker()


@pytest.fixture
def mock_background_tasks():
    return override_background_tasks


app.dependency_overrides[get_background_tasks] = override_background_tasks
app.state.aiograpi = True


def test_process_message():
    response = client.post(
        "/api/v1/messages",
        json={
            "message": "test: test",
            "action_params": {"id": "string"},
            "pushCategory": "string",
            "sourceUserId": 0,
            "intendedRecipientUserId": 0,
            "sender_username": "string",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Notification sent to bot in background."}
