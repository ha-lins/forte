#!/bin/bash
source activate texar
cd /data3/linshuai/manip_old/examples/text_content_manipulation

CUDA_VISIBLE_DEVICES=2 python manip_api.py\
 --attn_x --attn_y_ \
 --copy_x \
 --rec_w 0.8 \
 --coverage \
 --exact_cover_w 2.5 \
 --expr_name e2ev14_output/demo \
 --restore_from e2ev14_output/demo/ckpt/model.ckpt-921

source activate forte
cd /data3/linshuai/forte-rewriter/examples/generators/content_rewriter
