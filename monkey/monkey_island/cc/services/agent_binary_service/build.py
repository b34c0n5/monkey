import logging
from pathlib import Path

from common import DIContainer, OperatingSystem
from common.utils.file_utils import get_binary_io_sha256_hash
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.repositories import (
    FileRepositoryCachingDecorator,
    FileRepositoryLockingDecorator,
    FileRepositoryLoggingDecorator,
    IFileRepository,
    LocalStorageFileRepository,
    RetrievalError,
)
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH

from . import IAgentBinaryService
from .agent_binary_repository import AgentBinaryRepository
from .agent_binary_service import AgentBinaryService
from .event_handlers import reset_masque_on_island_mode_change
from .i_agent_binary_repository import IAgentBinaryRepository

AGENT_BINARIES_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries"
logger = logging.getLogger(__name__)


def build(container: DIContainer) -> IAgentBinaryService:
    agent_binary_repository = _build_agent_binary_repository()
    agent_binary_service = AgentBinaryService(agent_binary_repository)

    _register_event_handlers(container.resolve(IIslandEventQueue), agent_binary_service)

    return agent_binary_service


def _build_agent_binary_repository() -> IAgentBinaryRepository:
    file_repository = _decorate_file_repository(LocalStorageFileRepository(AGENT_BINARIES_PATH))
    agent_binary_repository = AgentBinaryRepository(file_repository)

    _log_agent_binary_hashes(agent_binary_repository)

    return agent_binary_repository


def _decorate_file_repository(file_repository: IFileRepository) -> IFileRepository:
    return FileRepositoryLockingDecorator(
        FileRepositoryLoggingDecorator(FileRepositoryCachingDecorator(file_repository))
    )


def _log_agent_binary_hashes(agent_binary_repository: IAgentBinaryRepository):
    """
    Logs all the hashes of the agent executables for debugging ease

    :param agent_binary_repository: Used to retrieve the agent binaries
    """
    agent_binaries = {
        "Linux": agent_binary_repository.get_agent_binary(OperatingSystem.LINUX),
        "Windows": agent_binary_repository.get_agent_binary(OperatingSystem.WINDOWS),
    }
    agent_hashes = {}

    for os, agent_binary in agent_binaries.items():
        try:
            binary_sha256_hash = get_binary_io_sha256_hash(agent_binary)
            agent_hashes[os] = binary_sha256_hash
        except RetrievalError as err:
            logger.error(f"No agent available for {os}: {err}")

    for os, binary_sha256_hash in agent_hashes.items():
        logger.info(f"{os} agent: SHA-256 hash: {binary_sha256_hash}")


def _register_event_handlers(
    island_event_queue: IIslandEventQueue, agent_binary_service: IAgentBinaryService
):
    island_event_queue.subscribe(
        IslandEventTopic.SET_ISLAND_MODE, reset_masque_on_island_mode_change(agent_binary_service)
    )