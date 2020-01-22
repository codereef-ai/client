#! /bin/bash

cr init demo-obj-detection-mlperf-coco-tf-cpu-benchmark-linux-portable-workflows \
        --name="Object detection; MLPerf inference; TensorFlow CPU; COCO; 5000 images validation; Linux; benchmark; Portable Workflows" \
        --tags="object-detection,mlperf,mlperf-inference,tensorflow,tensorflow-cpu,coco,5000,benchmark,linux,portable-workflows" \
        --workflow_repo_url="local" \
        --workflow="program:object-detection-tf-py-benchmark" \
        --workflow_cmd="default" \
	--workflow_cmd_extra="--repetitions=1 --env.CK_BATCH_SIZE=1 --env.CK_BATCH_COUNT=5000  --no_state_check" \
        --workflow_output_dir="tmp" \
        --desc_prereq="$PWD/prereq.txt" \
        --desc_prepare="$PWD/prepare.txt" \
        --add_extra_meta_from_file="$PWD/extra-meta.json" \
        --result_file="tmp/tmp-ck-timer.json" \
	--python_version_from="3.6" \
	--python_version_to="3.7.99" \
        --desc_graph="$PWD/graph-desc.json" \
        --graph_convertor="$PWD/graph-convertor.json" \
        --graphs="demo-obj-detection" \
#        --update_meta_and_stop