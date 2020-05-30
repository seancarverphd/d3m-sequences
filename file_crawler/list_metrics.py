import pickle

isCost = {
    'ACCURACY': False,
    'F1': False,
    'F1_MACRO': False,
    'MEAN_SQUARED_ERROR': True,
    'ROOT_MEAN_SQUARED_ERROR': True,
    'ROOT_MEAN_SQUARED_ERROR_AVG': True,
    'NORMALIZED_MUTUAL_INFORMATION': False,
    'MEAN_ABSOLUTE_ERROR': True,
    'OBJECT_DETECTION_AVERAGE_PRECISION': False
}

with open("pipelines.pickle", "rb") as f:
    pipe = pickle.load(f)

unique_metrics = list({p['metric'] for p in pipe})
print("unique_metrics = ", unique_metrics)
print("isCost[metric] =", [isCost[m] for m in unique_metrics])
