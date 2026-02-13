from typing import Any, Union
from fastapi.encoders import jsonable_encoder
import orjson


class ORJsonCoder:
    @staticmethod
    def encode(value: Any) -> bytes:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )

    @staticmethod
    def decode(value: Union[bytes | str]) -> Any:
        return orjson.loads(value)
