#! /bin/bash

cr init demo-obj-detection-mlperf-coco-tf-cpu-benchmark-linux-portable-workflows \
        --name="Object detection; MLPerf inference; TensorFlow CPU; COCO; Linux; benchmark; Portable Workflows" \
        --tags="object-detection,mlperf,mlperf-inference,tensorflow,tensorflow-cpu,coco,benchmark,linux,portable-workflows" \
        --workflow_repo_url="https://github.com/code-reef/ck-tensorflow-codereef" \
        --workflow="program:object-detection-tf-py-benchmark" \
        --workflow_cmd="default" \
	--workflow_cmd_extra="--repetitions=1 --env.CK_BATCH_SIZE=1 --env.CK_BATCH_COUNT=50" \
        --workflow_output_dir="tmp" \
        --desc_prereq="$PWD/prereq.txt" \
        --desc_prepare="$PWD/prepare.txt" \
        --add_extra_meta_from_file="$PWD/extra-meta.json" \
        --result_file="tmp/tmp-ck-timer.json" \
	--python_version_from="3.6" \
	--python_version_to="3.7.99" \
        --graphs="demo-obj-detection" 
#        --desc_graph="$PWD/graph-desc.json"
#        --update_meta_and_stop
