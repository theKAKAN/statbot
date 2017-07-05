#
# range.py
#
# statbot - Store Discord records for later analysis
# Copyright (c) 2017 Ammon Smith
#
# statbot is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import abc
import bisect

'''
This module contains the definitions for two classes: Range and MultiRange.
Both represent a contiguous sequence of comparable items without the need
to store every single possible element in between.

Range is simply a pair of a start and stop value that designate the inclusive
set of values in between that are seen as being within the range.

MultiRange is a sorted group of Ranges, allowing for a large, non-contiguous
set of values. Some operations on a Range will return this value if the result
isn't contiguous.

NullRange is a helper class that creates a Range that contains no members.
It is available as a precreated instance called NULL_RANGE.

AllRange is a helper class that creates a Range that contains all members.
It is available as a precreated instance called alll_range.

They all implement the AbstractRange base class, guaranteeing a certain set of
operations that can be performed on them.
'''

__all__ = [
    'AbstractRange',
    'Range',
    'MultiRange',
]

class AbstractRange:
    @abc.abstractmethod
    def min(self):
        '''
        Returns the smallest value in the range.
        '''

        pass

    @abc.abstractmethod
    def max(self):
        '''
        Returns the largest value in the range.
        '''

        pass

    @abc.abstractmethod
    def __or__(self, other):
        '''
        Returns the union between the two ranges.
        '''

        pass

    @abc.abstractmethod
    def __contains__(self, x):
        '''
        Determines if a value is within the range.
        '''

        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __hash__(self):
        pass

    @abc.abstractmethod
    def __bool__(self):
        pass

    # Default implementations
    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        if not isinstance(other, AbstractRange):
            raise TypeError(f"expected type 'AbstractRange', not '{type(other)!r}'")

        return self.min() <= other.min()

    def __lt__(self, other):
        if not isinstance(other, AbstractRange):
            raise TypeError(f"expected type 'AbstractRange', not '{type(other)!r}'")

        return self.min() < other.min()

    def __ge__(self, other):
        if not isinstance(other, AbstractRange):
            raise TypeError(f"expected type 'AbstractRange', not '{type(other)!r}'")

        return self.min() >= other.min()

    def __gt__(self, other):
        if not isinstance(other, AbstractRange):
            raise TypeError(f"expected type 'AbstractRange', not '{type(other)!r}'")

        return self.min() > other.min()

class Range(AbstractRange):
    '''
    A contiguous range of values, from a given starting to a given ending point.
    '''

    __slots__ = (
        'begin',
        'end',
    )

    def __init__(self, begin, end):
        if type(begin) != type(end):
            raise TypeError("type of both endpoints aren't the same")
        elif begin > end:
            raise ValueError("beginning value is larger than the end value")

        self.begin = begin
        self.end = end

    def min(self):
        return self.begin

    def max(self):
        return self.end

    def __contains__(self, item):
        return self.begin <= item <= self.end

    def __eq__(self, other):
        if isinstance(other, Range):
            return (self.begin == other.begin) and (self.end == other.end)
        elif isinstance(other, MultiRange):
            return other == self
        else:
            return False

    def __hash__(self):
        return hash(self.begin) ^ hash(self.end)

    def __bool__(self):
        # Ranges always have at least one item in them
        return True

class MultiRange(AbstractRange):
    '''
    A range of values, with support of discontinous jumps and other holes
    from the beginning to the end. This is implemented as a sorted list of
    Range objects.
    '''

    __slots__ = (
    )

    def __init__(self, *ranges):
        self.ranges = ranges

    def min(self):
        if self.ranges:
            return self.ranges[0].min()
        else:
            return None

    def max(self):
        if self.ranges:
            return self.ranges[-1].max()
        else:
            return None

    def __contains__(self, item):
        pass

    def __eq__(self, other):
        if isinstance(other, Range):
            return (len(self.ranges) == 1) and (self.ranges[0] == other)
        elif isinstance(other, MultiRange):
            return self.ranges == other.ranges
        else:
            return False

    def __hash__(self):
        return hash(self.ranges)

    def __bool__(self):
        return bool(self.ranges)

