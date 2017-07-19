#
# message_history.py
#
# statbot - Store Discord records for later analysis
# Copyright (c) 2017 Ammon Smith
#
# statbot is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

from .range import MultiRange, Range

__all__ = [
    'MessageHistory',
]

class MessageHistory(MultiRange):
    def __init__(self, *ranges):
        super().__init__(*ranges)

    def find_first_hole(self, start, max_size):
        for range in reversed(self.ranges):
            count = start - range.max()
            if count >= 0:
                return (current, min(count, max_size))

            current = range.min()
        return (current, max_size)

