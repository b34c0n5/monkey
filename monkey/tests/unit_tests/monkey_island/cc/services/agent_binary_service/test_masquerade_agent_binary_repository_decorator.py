import io

import pytest
from tests.monkey_island import InMemoryAgentBinaryRepository

from common import OperatingSystem
from monkey_island.cc.services.agent_binary_service.i_agent_binary_repository import (
    IAgentBinaryRepository,
)
from monkey_island.cc.services.agent_binary_service.masquerade_agent_binary_repository_decorator import (  # noqa: E501
    MasqueradeAgentBinaryRepositoryDecorator,
)

NULL_BYTES_LENGTH = 8
MASQUE = b"m0nk3y"

LINUX_AGENT_BINARY_BYTES = b"linux_binary"
LINUX_AGENT_BINARY = io.BytesIO(LINUX_AGENT_BINARY_BYTES)
MASQUED_LINUX_AGENT_BINARY = io.BytesIO(
    LINUX_AGENT_BINARY_BYTES + b"\x00" * NULL_BYTES_LENGTH + MASQUE
)

WINDOWS_AGENT_BINARY_BYTES = b"windows_binary"
WINDOWS_AGENT_BINARY = io.BytesIO(WINDOWS_AGENT_BINARY_BYTES)
MASQUED_WINDOWS_AGENT_BINARY = io.BytesIO(
    WINDOWS_AGENT_BINARY_BYTES + b"\x00" * NULL_BYTES_LENGTH + MASQUE
)


@pytest.fixture
def in_memory_agent_binary_repository() -> InMemoryAgentBinaryRepository:
    return InMemoryAgentBinaryRepository()


@pytest.fixture
def mock_masquerade_agent_binary_repository(
    in_memory_agent_binary_repository: IAgentBinaryRepository,
) -> MasqueradeAgentBinaryRepositoryDecorator:
    return MasqueradeAgentBinaryRepositoryDecorator(
        in_memory_agent_binary_repository, MASQUE, NULL_BYTES_LENGTH
    )


def test_masquerade_agent_binary_repository_decorator__linux(
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
):
    actual_linux_binary = mock_masquerade_agent_binary_repository.get_linux_binary()

    assert actual_linux_binary.getvalue() == MASQUED_LINUX_AGENT_BINARY.getvalue()  # type: ignore[attr-defined] # noqa: E501


def test_masquerade_agent_binary_repository_decorator__windows(
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
):
    actual_windows_binary = mock_masquerade_agent_binary_repository.get_windows_binary()

    assert actual_windows_binary.getvalue() == MASQUED_WINDOWS_AGENT_BINARY.getvalue()  # type: ignore[attr-defined] # noqa: E501


def test_masquerade_agent_binary_repository_decorator__cached_linux(
    in_memory_agent_binary_repository: InMemoryAgentBinaryRepository,
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
):
    actual_linux_binary = mock_masquerade_agent_binary_repository.get_linux_binary()
    in_memory_agent_binary_repository.agent_binaries[OperatingSystem.LINUX] = b"not_linux_binary"
    cached_linux_binary = mock_masquerade_agent_binary_repository.get_linux_binary()

    assert actual_linux_binary == cached_linux_binary


def test_masquerade_agent_binary_repository_decorator__cached_windows(
    in_memory_agent_binary_repository: InMemoryAgentBinaryRepository,
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
):
    actual_windows_binary = mock_masquerade_agent_binary_repository.get_windows_binary()
    in_memory_agent_binary_repository.agent_binaries[
        OperatingSystem.WINDOWS
    ] = b"not_windows_binary"
    cached_windows_binary = mock_masquerade_agent_binary_repository.get_windows_binary()

    assert actual_windows_binary == cached_windows_binary
