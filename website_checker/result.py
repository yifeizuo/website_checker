# Copyright (C) 2021 yifeizuo@gmail.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from datetime import datetime
import json


class WebsiteCheckResult(object):
    def __init__(self, status_code: int, response_time: float,
                 response_data_regex: str = None, is_regex_matched: bool = None,
                 check_timestamp: datetime = datetime.utcnow()):
        self.status_code = status_code
        self.response_time = response_time
        self.response_data_regex = response_data_regex
        self.is_regex_matched = is_regex_matched
        self.check_timestamp = check_timestamp

    def serialize(self) -> bytes:
        return json.dumps(self.result()).encode()

    @staticmethod
    def deserialize(result_bytes: bytes) -> WebsiteCheckResult:
        result_json = json.loads(result_bytes.decode())

        return WebsiteCheckResult(
            int(result_json.get("status_code")) if result_json.get("status_code") is not None else -1,
            float(result_json.get("response_time")) if result_json.get("response_time") is not None else -1.0,
            result_json.get("response_data_regex"),
            bool(result_json.get("is_regex_matched")) if result_json.get("is_regex_matched") is not None else None,
            datetime.fromisoformat(result_json.get("check_timestamp")) if result_json.get("check_timestamp") is not None else None,
        )

    def is_valid(self) -> bool:
        return self.check_timestamp is not None \
                and self.status_code != -1 \
                and self.response_time != -1.0

    def result(self) -> dict:
        """Result content to be inspected.

        Returns:
            dict: Content of the website check result
        """

        return {
            "status_code": str(self.status_code),
            "response_time": str(self.response_time),
            "response_data_regex": self.response_data_regex,
            "is_regex_matched": str(self.is_regex_matched) if self.is_regex_matched is not None else None,
            "check_timestamp": self.check_timestamp.isoformat(),
        }
