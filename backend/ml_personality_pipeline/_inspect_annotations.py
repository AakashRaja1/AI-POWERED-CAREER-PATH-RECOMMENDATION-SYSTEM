"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the  inspect annotations part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import pickle, pathlib
p=pathlib.Path('backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl')
print('exists',p.exists())
if p.exists():
    with open(p,'rb') as f:
        data=pickle.load(f, encoding='latin1')
    print('type',type(data))
    try:
        keys=list(data.keys())
        print('num keys',len(keys))
        print('sample keys',keys[:10])
    except Exception as e:
        print('error listing keys',e)
else:
    print('file not found')
