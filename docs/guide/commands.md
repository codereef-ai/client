# CodeReef Client commands

After installing the [CodeReef client](../getting-started/installation) you can use the following commands:





## CodeReef setup and low-level access

### Check the CodeReef client version

```
cr version
```

### Update CodeReef client dependencies (CK components)

```
cr update
```

### Setup the CodeReef account

*Setup your CodeReef account to be able to push new CodeReef components and results.*

```
cr setup --help
```

You can register your CodeReef account [here](https://codereef.ai/portal/account/signup/)
and get your *username* and *api_key* [here](https://codereef.ai/portal/user/settings/).

You can then setup your CodeReef account as follows:
```
cr setup --username="{above username}" --api_key="{above key}"
```

### Test the CodeReef login

*Test the login to the CodeReef portal*

```
cr login --help
```

After you setup your CodeReef account you can test the login as follows:
```
cr login
```

  access       CID:ck component identifier (repo UOA:)module UOA:data UOA
  start        Start CodeReef client to communicate with CodeReef server


### Access the open CodeReef API

*Test low-level access to the open CodeReef JSON API.*

```
cr access --help
```

You can access the [CodeReef JSON API](../resources/api) using input JSON file as follows:

```
cr access --filename=input.json
```

You can also write JSON dictionary in the command line while substituting *"* with *'*:
```
cr access --json="{'action':'login'}"
```

### Start the internal CodeReef server

*Run internal server on a user machine to automate the communication with the CodeReef portal.*

```
cr start
```

Note that you need to add flag "-h 0.0.0.0" if you start it from Docker:

```
cr start -h 0.0.0.0
```

See the demo of the CodeReef client communicating with the CodeReef portal to crowd-benchmark MLPerf:
[CodeReef.ai/demo](https://codereef.ai/demo).





## CodeReef CK components

### Download components

*Download a given CK component to your local CK repository.*

```
cr download --help
```

You can download a given [CK component](https://github.com/ctuning/ck) 
from the [CodeReef portal](https://codereef.ai/portal) 
with a given version using the following command:
```
cr download {module name}:{data name} (--version=1.0.0)
```

For example, you can download SSD-mobilenet package:
```
cr download package:model-tf-mlperf-ssd-mobilenet --version=1.0.0
```

You can use wildcards in the names of the CK components.

If this component already exists you can overwrite it by adding the flag "--force" or "-f".

You can download the CK component with all related dependencies by adding the flag "--all" or "-a". 
For example you can download program:cbench-automotive-susan with all related components 
and related data sets, and then immediately compile and run it as follows:
```
cr download program:cbench-automotive-susan --all
cr download dataset:* --tags="image,dataset"

ck compile program:cbench-automotive-susan --speed
ck run program:cbench-automotive-susan
```

### Publish components

*Publish/update CK component on the CodeReef portal.*


```
cr publish --help
```

You need to register at the CodeReef platform (similar to PyPI or GitHub)
to publish your components or update existing ones as described [here](#setup-the-codereef-account).

When you create new CK components or update existing ones, 
you can then publish the stable version on the [Codereef portal](https://codereef.ai/portal)
as follows:

```
cr publish {module name}:{data name} --version={version}
```

You can check the latest version of a given component at the CodeReef portal as follows:
```
cr versions {module name}:{data name}
```

You can specify extra options describing your component:
```
 --author TEXT
 --author_codereef_id TEXT
 --copyright TEXT
 --license TEXT
 --source TEXT
```

You can make this component private by specifying the flag "--private". 
In such case, it will be only visible for you or within your workgroups.

You can specify the list of workgroups for the published component using
the flag "--workspaces={list of CodeReef workspaces separated by comma}".

### List versions of a given component

*List versions of a given CK component at the CodeReef portal.*


```
cr versions --help
```

You can list all shared versions of a given CK component shared at the [Codereef portal](https://codereef.ai/portal)
as follows:

```
cr versions {module name}:{data name}
```

### Open a CodeReef web page with a given component

*Open a CodeReef web page with a given component.*


```
cr open {module name}:{data name}
```

## CodeReef dashboards

Our CodeReef portal supports customizable dashboards to support 
MLSysOps, collaborative experimentation, and live research papers.

### Initialize a CodeReef graph

*Create a new dashboard on the CodeReef platform.*

```
cr init-graph --help
```

You can check examples of public CodeReef dashboards [here](https://CodeReef.ai/portal/c/cr-result).
You can then create your own one as follows:
```
cr init-graph {some name for your dashboard} --version={version of your dashboard} --desc_file="$PWD/graph-desc.json"
```

Here is the example of the "graph-desc.json" to aggregate results from this [MLPerf crowd-benchmarking solution](https://codereef.ai/portal/c/cr-solution/demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows/):


```
{
    "default_key_x": "avg_time_ms",
    "default_key_y": "mAP",
    "default_sort_key": "avg_time_ms",
    "table_view": [
      {"key": "platform_info", "name": "Platform info", "json_and_pre": "yes", "skip_pre": "yes"},
      {"key": "resolved_deps", "name": "Resolved deps", "json_and_pre": "yes", "skip_pre": "yes"},
      {"key": "avg_fps", "type":"float", "format": "%.2f", "name": "Average FPS"},
      {"key": "avg_time_ms", "type":"float", "format": "%.2f", "name": "Average time (ms.)"},
      {"key": "detection_time_avg_s", "type":"float", "format": "%.2f", "name": "Detection time (average, sec.)"},
      {"key": "detection_time_total_s", "type":"float", "format": "%.2f", "name": "Detection time (total, sec.)"},
      {"key": "graph_load_time_s", "type":"float", "format": "%.2f", "name": "Graph load time (sec.)"},
      {"key": "images_load_time_avg_s", "type":"float", "format": "%.2f", "name": "Images load time (average, sec.)"},
      {"key": "images_load_time_total_s", "type":"float", "format": "%.2f", "name": "Images load time (total, sec.)"},
      {"key": "mAP", "type":"float", "format": "%.2f", "name": "mAP"},
      {"key": "metrics#DetectionBoxes_Precision/mAP", "type":"float", "format": "%.2f", "name": "Detection Boxes Precision mAP"},
      {"key": "metrics#DetectionBoxes_Precision/mAP (large)", "type":"float", "format": "%.2f", "name": "Detection Boxes Precision mAP (large)"},
      {"key": "metrics#DetectionBoxes_Precision/mAP (medium)", "type":"float", "format": "%.2f", "name": "Detection Boxes Precision mAP (medium)"},
      {"key": "metrics#DetectionBoxes_Precision/mAP (small)", "type":"float", "format": "%.2f", "name": "Detection Boxes Precision mAP (small)"},
      {"key": "metrics#DetectionBoxes_Precision/mAP@.50IOU", "type":"float", "format": "%.2f", "name": "Detection Boxes Precision mAP (.50 IOU)"},
      {"key": "metrics#DetectionBoxes_Precision/mAP@.75IOU", "type":"float", "format": "%.2f", "name": "Detection Boxes Precision mAP (.75 IOU)"},
      {"key": "metrics#DetectionBoxes_Recall/AR@1", "type":"float", "format": "%.2f", "name": "Detection Boxes Recall AR@1"},
      {"key": "metrics#DetectionBoxes_Recall/AR@10", "type":"float", "format": "%.2f", "name": "Detection Boxes Recall AR@10"},
      {"key": "metrics#DetectionBoxes_Recall/AR@100", "type":"float", "format": "%.2f", "name": "Detection Boxes Recall AR@100"},
      {"key": "metrics#DetectionBoxes_Recall/AR@100 (large)", "type":"float", "format": "%.2f", "name": "Detection Boxes Recall AR@100 (large)"},
      {"key": "metrics#DetectionBoxes_Recall/AR@100 (medium)", "type":"float", "format": "%.2f", "name": "Detection Boxes Recall AR@100 (medium)"},
      {"key": "metrics#DetectionBoxes_Recall/AR@100 (small)", "type":"float", "format": "%.2f", "name": "Detection Boxes Recall AR@100 (small)"},
      {"key": "recall", "type":"float", "format": "%.2f", "name": "Recall"},
      {"key": "setup_time_s", "type":"float", "format": "%.2f", "name": "Setup time (sec.)"},
      {"key": "test_time_s", "type":"float", "format": "%.2f", "name": "Test time (sec.)"},
      {"key": "solution_run_date", "type":"string", "format": "%Y-%m-%dT%H:%M:%SZ", "name": "Start date"},
      {"key": "solution_duration", "type":"float", "format": "%.2f", "name": "Total bechmark time (sec.)"}
    ]
}

```

### Push results

*Push results to existing CodeReef dashboards.*

```
cr push-result --help
```

You can push the new results to the [existing CodeReef dashboard](https://CodeReef.ai/portal/c/cr-result) as follows:


```
cr push-result {name of the existing dashboard} --json="[{'x':3,'y':-3}, {'x':4, 'y':5}]"

```
or
```
cr push-result {name of the existing dashboard} --file="$PWD/result.json"
```

where "result.json" file contains a list of dictionaries with results.





## CodeReef solutions

The CodeReef client helps to initialize, download, test and run [AI/ML solutions](https://codereef.ai/portal/c/cr-solution)
across diverse platforms as shown in this [CodeReef demo](https://codereef.ai/demo).

### Initialize a solution

*Download existing or start the new CodeReef solution*

```
cr init --help
```

You can download existing solution from this [list](https://codereef.ai/portal/c/cr-solution) as follows:

```
cr init demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows
```

Note that the CodeReef client will attempt to automatically download all required CK components 
(models, data sets, frameworks, packages, etc) and install missing software dependencies.
However, the installation of system packages is not yet automated and must be done manually 
(our future work).

### Run a solution

*Run initialized CodeReef solution*

```
cr run --help
```

After a given solution is initialized on a user machine, it is possible to run it as follows:
```
cr run {name of the CodeReef solution}
```

For example, it is possible to run the MLPerf inference benchmarking solution as follows:

```
cr init demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows
```

### Benchmark a solution

*Crowd-benchmark the CodeReef solution and share results on a CodeReef dashboard*

```
cr benchmark --help
```

When a given solution is initialized and can run on a given machine, it is possible
to participate in crowd-benchmarking and share results (speed, accuracy, energy, costs
and other exposed characteristics) using CodeReef dashboards similar to SETI@home.

Do not forget to setup your CodeReef account using "cr setup" before participating
in crowd-benchmarking.

For example, it is possible to participate in collaborative validation
of MLPerf inference benchmarking as follows:

```
cr benchmark demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows
```

You can view the crowd-benchmarked results and compare with the official ones 
at this [public CodeReef dashboard](https://codereef.ai/portal/c/cr-result/sota-mlperf-object-detection-v0.5-crowd-benchmarking).

We are also working on a user-friendly GUI to enable MLSysOps and monitor ML in production
as shown in this [demo](https://codereef.ai/demo).

### Activate a virtual environment for the solution

*Activate virtual environment for a given solution*

```
cr activate --help
```

After a given solution is initialized, all required software is detected and all missing packages are installed, 
it is possible to activate the virtual environment for this solution to continue testing and debugging it as follows:

```
cr activate {name of the CodeReef solution}
```

Example:
```
cr activate demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows
```

You can then use [CK](https://github.com/ctuning/ck) as well as the CodeReef client
to improve/update this solution. 

We plan to provide a tutorial about that.

### List local solutions

You can list all local solutions using the following command:

```
cr ls
```

### Find local solutions

You can find the place where a given local solution is initialized together 
with all the components and a virtual environment as follows:

```
cr find {name of the CodeReef solution}
```

Example:
```
cr find demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows
```

### Delete local solutions

You can delete a locally initialized solution as follows:

```
cr rm {name of the CodeReef solution}
```

Example:

```
cr rm demo-obj-detection-coco-tf-cpu-benchmark-linux-portable-workflows
```
