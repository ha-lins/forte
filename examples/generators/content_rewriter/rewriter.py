#!/bin/bash
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
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor
from ft.onto.base_ontology import Utterance, UtteranceContext
import subprocess
import os

class ContentRewriter(PackProcessor):
    def _process(self, input_pack: DataPack):
        context = input_pack.get_single(UtteranceContext)
        utterance = input_pack.get_single(Utterance)

        # Step 1: prepare the input data file
        type = []
        val = []
        asso = []
        # print(context.text)

        for triple in context.text.split():
            # print(triple)
            for idx, i in enumerate(triple.split('|')):
                if not idx:
                    val.append(i)
                elif idx == 1:
                    type.append(i)
                else:
                    asso.append(i)
        data_dir = '/data3/linshuai/manip_old/examples/text_content_manipulation/e2ev14_demo/test'
        with open('{}/x_type.test.txt'.format(data_dir), 'w') as f_type, \
                open('{}/x_value.test.txt'.format(data_dir), 'w') as f_val, \
                open('{}/x_associated.test.txt'.format(data_dir), 'w') as f_asso, \
                open('{}/y_ref.test.txt'.format(data_dir), 'w') as f_ref:
            f_type.write(' '.join(type))
            f_val.write(' '.join(val))
            f_asso.write(' '.join(asso))
            f_ref.write(utterance.text)

        # Step 2: Restore the generation model and test
        os.system('./run.sh')

        # step 3: process the output file
        output_dir = '/data3/linshuai/manip_old/examples/text_content_manipulation/e2ev14_output'
        with open('{}/demo/ckpt/hypos.step921.test.txt'.format(output_dir), 'r') as f_hypo:
            hypo = f_hypo.read()

        response = hypo.replace("_", " ")
        # print('Now you can use the utterance and context to do prediction')

        print('The input context/table is:{}'.format(context.text))


        print('The utterance is:{}'.format(utterance.text.replace('_', ' ')))

        print('Generation sentence:{}'.format(response))

        # First add the text here.
        input_pack.set_text(input_pack.text + '\n' + response)
        # And then mark this as a new utterance.
        Utterance(input_pack,
                  len(input_pack.text) - len(response),
                  len(input_pack.text))
