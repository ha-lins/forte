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
The re-writer processor
"""
import os
from typing import Dict, Any, Optional
import logging

from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor
from ft.onto.base_ontology import ClinicalEntityMention

# from examples.Cliner.CliNER.code import predict#, train, evaluate
from examples.Cliner.CliNER.code.predict import *

class ClinicalNER(PackProcessor):
    def initialize(self, resources: Resources, configs: Config):
        # Setup model path.
        self.txt = os.path.join(
            configs.model_dir, 'data/examples/test_ex_doc.txt')
        self.output = os.path.join(  # type: ignore
            configs.model_dir, 'data/test_predictions')
        self.model_path = os.path.join(  # type: ignore
            configs.model_dir, 'models/foo.model')
        self.format = 'i2b2'
        # pylint: disable=attribute-defined-outside-init
        self.model = CliNERPredict(self.txt, self.output, self.model_path, self.format)

    def prepare_data(self, clinical_text: str):
        with open(self.txt, 'w') as file:
            file.write(clinical_text)


    def _process(self, input_pack: DataPack):
        doc = input_pack.text

        self.prepare_data(doc)
        # print(doc)

        self.model.predict()
        
        # self.prepare_data()
        con = codecs.open(self.output, "r", encoding="utf8")

        ner_labels = []
        for line in con:
            labels = {}
            temp_labels = line[2:].strip().split('||')
            labels['type'] = temp_labels[1][3:-1]
            name_and_span = temp_labels[0].split('"')
            labels['name'] = name_and_span[1][0:]
            labels['span_begin'] = name_and_span[2].split()[0]
            labels['span_end'] = name_and_span[2].split()[1]
            labels['line_num'] = name_and_span[2].split()[0].split(':')[0]
            print(labels)
            ner_labels.append(labels)
    
        offsets = []
        offset = 0
        text = ""
        text_lines = []
    
        for i, line in enumerate(doc):
            text += line
            offsets.append(offset)  # the begin of the text
            offset += len(line) + 1
            text_lines.append(line)
    
        for labels in ner_labels:
            line_num = int(labels['line_num']) - 1
            text_line = text_lines[line_num]
            print(line_num, offsets)
            span_begin = text_line.split()[int(labels['span_begin'].split(':')[1])]
            word_begin = offsets[line_num] + text_line.index(span_begin)
    
            word_end = word_begin + len(labels['name'])
            entity = ClinicalEntityMention(input_pack, word_begin,
                                           word_end)
            entity.cliner_type = labels['type']

        input_pack.set_text(text, replace_func=self.text_replace_operation)
    
        Document(input_pack, 0, len(text))

        input_pack.pack_name = 'Cliner_input'
    


    # def prepare_data(self, context: UtteranceContext, utterance: Utterance):
    #     logging.info("Preparing test data with the context and utterance")
    #     logging.info("Context is : %s", context.text)
    #     logging.info("Utterance is : %s", utterance.text)
    #
    #     type = []
    #     val = []
    #     asso = []
    #
    #     for triple in context.text.split():
    #         for idx, i in enumerate(triple.split('|')):
    #             if not idx:
    #                 val.append(i)
    #             elif idx == 1:
    #                 type.append(i)
    #             else:
    #                 asso.append(i)
    #     data_dir = os.path.join(config_data_e2e_clean.dataset_dir, 'test')
    #     logging.info('Writing to data dir: %s', data_dir)
    #
    #     with open('{}/x_type.test.txt'.format(data_dir), 'w') as f_type, \
    #             open('{}/x_value.test.txt'.format(data_dir), 'w') as f_val, \
    #             open('{}/x_associated.test.txt'.format(data_dir),
    #                  'w') as f_asso, \
    #             open('{}/y_ref.test.txt'.format(data_dir), 'w') as f_ref:
    #         f_type.write(' '.join(type))
    #         f_val.write(' '.join(val))
    #         f_asso.write(' '.join(asso))
    #         f_ref.write(utterance.text)

    @classmethod
    def default_configs(cls) -> Dict[str, Any]:
        config = super().default_configs()
        config['model_dir'] = 'content_rewriter/model'
        return config
