# Copyright 2019 The Forte Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
The reader to read a table and example utterance.
"""
from typing import Iterator, Tuple
import codecs
import os

from forte.data.data_pack import DataPack
from forte.data.readers.base_reader import PackReader
from ft.onto.base_ontology import ClinicalEntityMention, Token, Sentence, Document


class ClinerReader(PackReader):
    def _collect(self, txt_path: str, con_path: str  # type: ignore
                 ) -> Iterator[Tuple[str, str]]:
        yield txt_path, con_path

    def _parse_pack(self, collection) -> Iterator[DataPack]:
        txt_path, con_path = collection

        pack = self.new_pack(pack_name='Cliner_input')
        doc = codecs.open(txt_path, "r", encoding="utf8")
        # con = codecs.open(con_path, "r", encoding="utf8")
        #
        # ner_labels = []
        # for line in con:
        #     # token = Token(pack, word_begin, word_end)
        #     labels = {}
        #     temp_labels = line[2:].strip().split('||')
        #     labels['type'] = temp_labels[1][3:-1]
        #     name_and_span = temp_labels[0].split('"')
        #     labels['name'] = name_and_span[1][0:]
        #     labels['span_begin'] = name_and_span[2].split()[0]
        #     labels['span_end'] = name_and_span[2].split()[1]
        #     labels['line_num'] = name_and_span[2].split()[0].split(':')[0]
        #     print(labels)
        #     ner_labels.append(labels)
        #
        # offsets = []
        # offset = 0
        # text = ""
        # text_lines = []
        #
        # for i, line in enumerate(doc):
        #     text += line
        #     offsets.append(offset)  # the begin of the text
        #     offset += len(line) + 1
        #     text_lines.append(line)
        #
        # for labels in ner_labels:
        #     line_num = int(labels['line_num']) - 1
        #     text_line = text_lines[line_num]
        #     print(line_num, offsets)
        #     span_begin = text_line.split()[int(labels['span_begin'].split(':')[1])]
        #     word_begin = offsets[line_num] + text_line.index(span_begin)
        #
        #     word_end = word_begin + len(labels['name'])
        #     entity = ClinicalEntityMention(pack, word_begin,
        #                                    word_end)
        #     entity.cliner_type = labels['type']
        #
        # pack.set_text(text, replace_func=self.text_replace_operation)
        #
        # Document(pack, 0, len(text))
        #
        # pack.pack_name = 'Cliner_input'
        #
        # yield pack


