## A Content Re-writer Example

This example implements a content rewriter. Given a table and a sentence, this
will rewrite the sentence based on the table.

Run `pipeline.py` to execute the rewriter. The other files are:
 - `reader.py`: reads the data.
 - `reweriter.py`: conducts the actual rewriting.

### Prerequisites

The code has been tested on:
`Python==3.6.0, tensorflow-gpu==1.12.0, texar==0.2.1, texar-pytorch==0.1.1`

Run the following commands:

```bash
cd model
pip3 install -r requirements.txt
```

You also need to install texar-tf from the [link](https://github.com/asyml/texar/archive/v0.2.1.zip). Please ensure that texar and texar-pytorch are both installed from source using this command (without -e):

```bash
cd texar && pip3 install .
```


### Downloading the models and data

Before we run the rewriting demo, we need to download models and data from the [link](https://drive.google.com/drive/folders/1jNaJ_R_f89G8xbAC8iwe49Yx_Z-LXr0i?usp=sharing) and put the two directories(i.e., e2e_data, e2e_model) under the current `model/` directory.  

### Running the example

Now to see the example in action, just run

```bash
python pipline.py
```