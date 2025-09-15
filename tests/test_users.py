import pytest
from app.db.models import Users
from app.db.enums import WarningSeverity

@pytest.mark.asyncio
async def test_user_creation(test_user):
    assert len(str(test_user.user_id)) == 8
    assert len(test_user.unique_code) == 5
    assert test_user.warning_count == 0
    assert test_user.is_blocked == False
    assert test_user.created_at


@pytest.mark.asyncio
async def test_add_warning(test_user):
    from app.db.models.admins import Admins
    from app.db.enums import AdminRole

    test_admin = await Admins.create(
            admin_user_id=123456789,
            role=AdminRole.SUPER
    )
    warning = await test_user.add_warning(
            reason="Test warning",
            severity=WarningSeverity.MEDIUM,
            issued_by=test_admin,

    )

    await test_user.refresh_from_db()
    assert test_user.warning_count == 1
    assert warning.reason == "Test warning"
    assert warning.severity == WarningSeverity.MEDIUM