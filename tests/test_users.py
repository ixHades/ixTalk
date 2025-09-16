import pytest
from iso8601.test_iso8601 import test_parse_no_timezone_different_default

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

    test_admin = await Admins.create(admin_user_id=123456789, role=AdminRole.SUPER)
    warning = await test_user.add_warning(
        reason="Test warning",
        severity=WarningSeverity.MEDIUM,
        issued_by=test_admin,
    )

    await test_user.refresh_from_db()
    assert test_user.warning_count == 1
    assert warning.reason == "Test warning"
    assert warning.severity == WarningSeverity.MEDIUM


@pytest.mark.asyncio
async def test_is_blocked_or_high_warning(test_user):
    test_user.is_blocked = True
    assert await test_user.is_blocked_or_high_warning() == True
    test_user.is_blocked = False
    from app.db.models.admins import Admins
    from app.db.enums import AdminRole

    test_admin = await Admins.create(admin_user_id=164465465, role=AdminRole.SUPER)
    warning = await test_user.add_warning(
        reason="Test warning",
        severity=WarningSeverity.HIGH,
        issued_by=test_admin,
    )
    assert test_user.warning_count == 1
    assert warning.reason == "Test warning"
    assert warning.severity == WarningSeverity.HIGH


async def test_get_active_warnings(test_user, test_admin):
    await test_user.add_warning(
        reason="Test warning",
        severity=WarningSeverity.HIGH,
        issued_by=test_admin,
    )
    assert len(await test_user.get_active_warnings()) == 1
    assert isinstance(await test_user.get_active_warnings(), list)
    assert isinstance(await test_user.warning_entries.all(), list)


async def test_regenerate_code(test_user):
    old_code = test_user.unique_code
    assert await test_user.regenerate_unique_code() != old_code
