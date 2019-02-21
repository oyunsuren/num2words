# -*- encoding: utf-8 -*-
# Copyright (c) 2019, Engineersoft LLC.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from num2words.base import Num2Word_Base
from num2words.utils import get_digits, splitby3

ZERO = 'тэг'

ONES = {
    1: ('нэг', 'нэгэн',),
    2: ('хоёр',),
    3: ('гурав', 'гурван',),
    4: ('дөрөв', 'дөрвөн',),
    5: ('тав', 'таван',),
    6: ('зургаа', 'зургаан',),
    7: ('долоо', 'долоон',),
    8: ('найм', 'найман',),
    9: ('ес', 'есөн',),	
}

TENS = {
    1: ('арван',),
    2: ('хорин',),
    3: ('гучин',),
    4: ('дөчин',),
    5: ('тавин',),
    6: ('жаран',),
    7: ('далан',),
    8: ('наян',),
    9: ('ерэн',),
}

HUNDREDS = 'зуун'

THOUSANDS = {
    1: ('мянга', 'мянган'),  # 10^3
    2: ('сая',),  # 10^6
    3: ('тэр бум',),  # 10^9
    4: ('их наяд',),  # 10^12
    5: ('тунамал',),  # 10^15
    6: ('их ингүмэл',),  # 10^18
    7: ('ялгаруулагч',),  # 10^21
    8: ('их өвөр дээр',),  # 10^24
    9: ('хязгаар үзэгдэл',),  # 10^27
    10: ('их шалтгааны үзэгдэл',),  # 10^30
}

class Num2Word_MN(Num2Word_Base):

    def setup(self):
        self.negword = "хасах"
        self.pointword = "цэг"
        self.errmsg_nornum = "Зөвхөн тоог үсэг рүү хөрвүүлнэ."
        self.exclude_title = ["цэг", "хасах"]
		
    def set_numwords(self):
        # @FIXME
        self.cards[0] = []

    def to_cardinal(self, number):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            return u'%s %s %s' % (
                self._int2word(int(left)),
                self.pointword,
                self._int2word(int(right))
            )
        else:
            return self._int2word(int(n))

    def _int2word(self, n):
        if n < 0:
            return ' '.join([self.negword, self._int2word(abs(n))])

        if n == 0:
            return ZERO

        words = []
        chunks = list(splitby3(str(n)))
        i = len(chunks)
        for x in chunks:
            i -= 1
            n1, n2, n3 = get_digits(x)

            if n3 > 2:
                words.append(ONES[n3][1])
            elif n3 > 0:
                words.append(ONES[n3][0])
				
            if n3 > 0:
                words.append(HUNDREDS)

            if n2 > 0:
                words.append(TENS[n2][0])

            if (n1 == 2) or (n1 == 1 and i > 0):
                words.append(ONES[n1][0])
            elif n1 > 0:
                words.append(ONES[n1][1])		    

            if i > 0 and x != 0:
                words.append(THOUSANDS[i][0])

        if words[-1] == THOUSANDS[1][0]:
            words[-1] = THOUSANDS[1][1]

        return ' '.join(words)
