#
# Copyright (c) 2018-2020 Bahtiar `kalkin-` Gadimov.
#
# This file is part of Git Log Viewer
# (see https://github.com/kalkin/git-log-viewer).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
''' Status bar ui stuff '''
from typing import List, Optional, Tuple

from prompt_toolkit.filters import Condition
from prompt_toolkit.layout import (BufferControl, ConditionalContainer,
                                   UIContent, Window)
from prompt_toolkit.layout.controls import GetLinePrefixCallable


class StatusContent(UIContent):
    '''
        A status bar consisting of one line
    '''

    # pylint: disable=too-few-public-methods

    def __init__(self):
        def get_line(_: int) -> List[Tuple[str, str]]:
            result = self.text.strip()
            length = len(result)
            diff = self.width - length
            if diff >= 0:
                result += ' ' * diff
            else:
                result = result[:length - diff]
                result += '…'

            return [('bg:ansiblue ansiwhite', result)]

        super().__init__(line_count=1, get_line=get_line)
        self.text = ''
        self.width = 0

    def get_height_for_line(self,
                            lineno: int,
                            width: int,
                            get_line_prefix: Optional[GetLinePrefixCallable],
                            slice_stop: Optional[int] = None) -> int:
        return 1


class StatusBar(BufferControl):
    ''' Status bar implementation '''
    def __init__(self):
        super().__init__(focusable=False)
        self.content = StatusContent()

    def set_status(self, text: str) -> None:
        ''' Set some text to show in the status bar '''
        self.content.text = text

    def clear(self) -> None:
        ''' Clear the content of the status bar '''
        self.content.text = ''

    def create_content(self,
                       width: int,
                       height: int,
                       preview_search: bool = False) -> UIContent:
        self.content.width = width
        return self.content


STATUS = StatusBar()


@Condition
def statis_is_visible() -> bool:
    ''' Return `True` if status line is visible '''
    return bool(STATUS.content.text)


STATUS_WINDOW = ConditionalContainer(content=Window(content=STATUS,
                                                    height=1,
                                                    ignore_content_height=True,
                                                    wrap_lines=False),
                                     filter=statis_is_visible)
