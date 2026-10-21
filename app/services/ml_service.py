import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(values: list[float]) -> dict:
    if len(values) < 2:
        return {"anomalies_detected": [], "scores": []}
        
    X = np.array(values).reshape(-1, 1)
    clf = IsolationForest(contamination=0.2, random_state=42)
    preds = clf.fit_predict(X)
    scores = clf.decision_function(X).tolist()
    
    # IsolationForest predicts -1 for anomalies and 1 for normal data points
    anomalies = [i for i, pred in enumerate(preds) if pred == -1]
    
    return {
        "anomalies_detected": anomalies,
        "scores": scores
    }