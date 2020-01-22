# Practical use cases and tutorials

We gradually update and improve this section with the help of our users.
Feel free to extend it via [GitHub pull-requests](https://github.com/codereef-ai/client).



## Share and reuse CK components similar to PyPI

[Collective Knowledge framework (CK)](https://github.com/ctuning/ck) was introduced in 2015 
to provide a common format for research artifacts and enable portable workflows.

The idea behind CK is to convert ad-hoc research projects into a file-based database 
of reusable components (code, data, models, pre-/post-processing scripts, experimental results, R&D
automation actions and best research practices to reproduce results, 
and live papers) with unified Python APIs, CLI-based actions, JSON meta
information and JSON input/output.

CK also features plugins to automatically detect required software, models and datasets 
on a user machine and install (cross-compile) the missing ones while supporting
different operating systems (Linux, Windows, MacOS, Android)
and hardware (Nvidia, Arm, Intel, AMD ...).

Unified CK API helps researchers to connect their artifacts into
automated workflows instead of some ad-hoc scripts while making them
[portable](https://codereef.ai/portal/c/program) 
using the automatic [software detection plugins](https://codereef.ai/portal/c/soft) and
[meta-packages](https://codereef.ai/portal/c/soft).

While using CK to help researchers share their artifacts during [reproducibility initiatives at ML and systems conferences](https://cTuning.org/ae)
(see [15+ artifacts](https://codereef.ai/portal/search/?q=%22reproduced-papers%22%20AND%20%22portable-workflow-ck%22) shared by researchers in the CK format) 
and companies to [automate ML benchmarking and move ML models to production](https://youtu.be/1ldgVZ64hEI) we noticed two major limitations: 
  
* The distributed nature of the CK technology, the lack of a centralized place to keep all CK components and the lack of convenient GUIs makes it very challenging to keep track of all contributions from the community, add new components, assemble workflows, automatically test them across diverse platforms, and connect them with legacy systems.

* The concept of backward compatibility of CK APIs and the lack of versioning similar to Java made it very challenging to keep stable and bug-free workflows in real life - a bug in a CK component from one GitHub project can easily break dependent ML workflows in another GitHub project.

These issues motivated us to develop CodeReef as an open web platform to aggregate, version and test all CK components 
and portable CK workflows necessary to enable portable MLOps with the automated deployment of ML models 
in production across diverse systems from IoT to data centers in the most efficient way (MLSysOps).

You need to install the [CodeReef client](../getting-started/installation) 
and then follow [this guide](commands.html#codereef-ck-components) to 
learn how to download or upload your CK components. 



## Create customizable dashboards for live papers and collaborative experiments

We created CK also to support [auto-generated and live papers](https://codereef.ai/portal/search/?q=%22live-paper%22),
[collaborative experiments](https://codereef.ai/portal/search/?q=%22reproduced-results%22),
[reproducible optimization tournaments](https://cKnowledge.org/request)
and [crowd-benchmarking](https://codereef.ai/portal/c/cr-result/sota-mlperf-object-detection-v0.5-crowd-benchmarking)

The users can now create customizable dashboards on CodeReef platform
and push their results. Please follow [this guide](commands.html##codereef-dashboards) to learn
how to create such dashboards.

You can also check our [MLPerf demo](https://CodeReef.ai/demo) 
with [crowd results](https://codereef.ai/portal/c/cr-result/sota-mlperf-object-detection-v0.5-crowd-benchmarking/).




## Use cross-platform software detection plugins

*To be updated. Note that we plan to provide a GUI to add new CK components.*

See the list of [shared software detection plugins](https://codereef.ai/portal/c/soft) with usage examples.

See examples of MLPerf inference benchmark automation using CodeReef and CK 
for [Linux](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows/#prerequisites),
[Raspberry Pi](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-rpi-portable-workflows/#prerequisites) 
and [Android](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tflite-cpu-benchmark-android-portable-workflows/#prerequisites).



## Use cross-platform meta packages

*To be updated. Note that we plan to provide a GUI to add new CK components.*

See the list of [shared meta packages](https://codereef.ai/portal/c/package) with usage examples.

See examples of MLPerf inference benchmark automation using CodeReef and CK 
for [Linux](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows/#prerequisites),
[Raspberry Pi](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-rpi-portable-workflows/#prerequisites) 
and [Android](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tflite-cpu-benchmark-android-portable-workflows/#prerequisites).




## Use portable workflows

*To be updated. Note that we plan to provide a GUI to add new CK components.*

See the list of [shared program workflows](https://codereef.ai/portal/c/program) with usage examples.

See examples of MLPerf inference benchmark automation using CodeReef and CK 
for [Linux](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows/#prerequisites),
[Raspberry Pi](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-rpi-portable-workflows/#prerequisites) 
and [Android](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tflite-cpu-benchmark-android-portable-workflows/#prerequisites).




## Prepare portable CodeReef ML solutions

*To be updated. Note that we plan to provide a GUI to add new CK components.*

See the list of [shared CodeReef solutions](https://codereef.ai/portal/c/program) and the [MLPerf automation demo](https://CodeReef.ai/demo).

Please follow [this guide](commands.html#codereef-solutions) and check this 
[MLPerf inference benchmark automation example](https://github.com/codereef-ai/client/tree/master/examples/codereef-solution-mlperf-inference-0.5).
