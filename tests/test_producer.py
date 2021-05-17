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
from unittest import mock
import website_checker


class TestProducer(object):
    def set_up(self):
        pass

    def test_check(self, requests_mock):
        requests_mock.get('http://test-url', text='test data - test-regex-pattern', status_code=400,)
        mocked_producer = mock.Mock()
        test_checker = website_checker.WebsiteChecker(
            mocked_producer,
            check_interval_in_seconds="123",
            check_url="http://test-url",
            check_regex="test-regex-pattern"
        )

        result: website_checker.WebsiteCheckResult = test_checker.check()

        assert result.status_code == 400
        assert result.response_time > 0
        assert result.check_timestamp is not None
        assert result.is_regex_matched is True
        assert result.response_data_regex == "test-regex-pattern"

    def tear_down(self):
        pass
