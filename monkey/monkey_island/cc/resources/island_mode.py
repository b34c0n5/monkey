import json
import logging
from http import HTTPStatus

from flask import make_response, request

from monkey_island.cc.models import IslandMode as IslandModeEnum
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services import IslandModeService

logger = logging.getLogger(__name__)


class IslandMode(AbstractResource):
    urls = ["/api/island/mode"]

    def __init__(self, island_mode_service: IslandModeService):
        self._island_mode_service = island_mode_service

    @jwt_required
    def put(self):
        try:
            body = json.loads(request.data)
            mode = IslandModeEnum(body.get("mode"))

            self._island_mode_service.set_mode(mode)

            # TODO: Do any of these returns need a body and make_response? What happens if we just
            #       return the response code?
            # API Spec: This should be 204 (NO CONTENT)
            return make_response({}, HTTPStatus.NO_CONTENT)
        except (AttributeError, json.decoder.JSONDecodeError):
            return make_response({}, HTTPStatus.BAD_REQUEST)
        except ValueError:
            return make_response({}, HTTPStatus.UNPROCESSABLE_ENTITY)

    @jwt_required
    def get(self):
        island_mode = self._island_mode_service.get_mode()
        return make_response({"mode": island_mode.value}, HTTPStatus.OK)
