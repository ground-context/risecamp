#!/usr/bin/env python
import pandas as pd
import numpy as np
from ground.client import GroundClient

### DATA TRANSFORMATION

# declare the input and output file variables
SOURCE_FILE = 'data.txt'
DEST_FILE = 'split_data.csv'

# create a dataframe with the data from the source file
df = pd.read_csv(SOURCE_FILE, header=None)

# apply a transformation that splits the input into three columns
df = df[0].apply(lambda x: pd.Series([i for i in x.split()]))

# write the resulting output to the dest file
df.to_csv(path_or_buf=DEST_FILE, header=False, index=False)

### GROUND INSTRUMENTATION

# initialize Ground client
gc = GroundClient()

# create a new node & node version for the dest file; we assume that the source
# file was already registered
node_id = gc.createNode(DEST_FILE, DEST_FILE)['id']
dst_nv_id = gc.createNodeVersion(node_id, tags={'tag': {'key': 'tag', 'value':
    'congratulations, you found the tag!', 'type': 'string'}})['id']

# retrieve the node version id of the source file
src_nv_id = gc.getNodeLatestVersions(SOURCE_FILE)[0]

# create a new lineage edge
le_key = SOURCE_FILE + '_to_' + DEST_FILE
le_id = gc.createLineageEdge(le_key, le_key)['id']

# get the id of the most recent commit of this repo
git_id = gc.getNodeLatestVersions('risecamp')[0]
git_sha = gc.getNodeVersion(git_id)['tags']['commit']['value']

# create a new lineage edge version connecting the source file to the dest file
gc.createLineageEdgeVersion(le_id, src_nv_id, dst_nv_id, {'git_commit': {'key':
    'git_commit', 'value': git_sha, 'type': 'string'}})

# acknowledge completion
print("Succesfully transformed " + SOURCE_FILE + "!")
