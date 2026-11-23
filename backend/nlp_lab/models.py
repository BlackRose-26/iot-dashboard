"""Local-only research models. No web inference, private data or runtime activation."""
import time

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion


class Heads:
    def fit(self,features,rows):
        self.primary=LogisticRegression(class_weight='balanced',max_iter=1500,random_state=20261120)
        self.primary.fit(features,[r['target']['topic'] for r in rows])
        self.subtypes={}
        for topic in ('knowledge','social','definition'):
            indices=[i for i,r in enumerate(rows) if r['target']['topic']==topic]
            labels=[rows[i]['label'].split(':',1)[1] for i in indices]
            if not indices: continue
            if len(set(labels))==1: self.subtypes[topic]=labels[0];continue
            classifier=LogisticRegression(class_weight='balanced',max_iter=1500,random_state=20261120)
            classifier.fit(features[indices],labels)
            self.subtypes[topic]=classifier
        return self

    def predict(self,features):
        probabilities=self.primary.predict_proba(features)
        labels=[]
        for i,index in enumerate(probabilities.argmax(axis=1)):
            topic=self.primary.classes_[index]
            classifier=self.subtypes.get(topic)
            subtype=classifier if isinstance(classifier,str) else classifier.predict(features[i:i+1])[0] if classifier is not None else None
            labels.append(topic+(':'+str(subtype) if topic in ('knowledge','social','definition') else ''))
        return labels,probabilities


class SparseModel:
    def __init__(self):
        self.encoder=FeatureUnion([
            ('words',TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True,max_features=20000)),
            ('characters',TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),sublinear_tf=True,max_features=30000))])
    def fit(self,texts,rows):
        self.heads=Heads().fit(self.encoder.fit_transform(texts),rows)
        return self
    def predict(self,texts): return self.heads.predict(self.encoder.transform(texts))


class DenseModel:
    def __init__(self,encoder): self.encoder=encoder
    def encode(self,texts):
        return self.encoder.encode(texts,batch_size=16,normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
    def fit(self,texts,rows): self.heads=Heads().fit(self.encode(texts),rows);return self
    def predict(self,texts): return self.heads.predict(self.encode(texts))


def scaled(probabilities,temperature):
    logits=np.log(np.clip(probabilities,1e-12,1))/temperature
    logits-=logits.max(axis=1,keepdims=True)
    values=np.exp(logits)
    return values/values.sum(axis=1,keepdims=True)


def fit_temperature(probabilities,truth,classes):
    from scipy.optimize import minimize_scalar
    indices=np.array([list(classes).index(t) for t in truth])
    def loss(t): return float(-np.log(np.clip(scaled(probabilities,t)[np.arange(len(indices)),indices],1e-12,1)).mean())
    result=minimize_scalar(loss,bounds=(.25,5),method='bounded')
    return {'temperature':float(result.x),'calibration_n':len(indices),
            'calibration_log_loss_before':loss(1),'calibration_log_loss_after':loss(result.x)}


def policy(probabilities,truth,classes):
    """Choose operating thresholds on calibration only; no comparison labels."""
    best=None
    for confidence in (.35,.50,.65,.80,.90):
        for margin in (.00,.10,.20):
            ordered=np.sort(probabilities,axis=1)
            accepted=(ordered[:,-1]>=confidence)&(ordered[:,-1]-ordered[:,-2]>=margin)
            predicted=np.asarray(classes)[probabilities.argmax(axis=1)]
            answers=accepted&(predicted!='unsupported')
            false_accepts=int(np.sum(answers&(np.asarray(truth)=='unsupported')))
            correct=int(np.sum(answers&(predicted==np.asarray(truth))))
            precision=correct/int(answers.sum()) if answers.sum() else None
            if answers.sum() and precision>=.90 and false_accepts==0:
                candidate={'confidence':confidence,'margin':margin,'calibration_answers':int(answers.sum()),
                           'calibration_primary_precision':precision,'calibration_false_accepts':false_accepts}
                if best is None or candidate['calibration_answers']>best['calibration_answers']: best=candidate
    return best or {'confidence':1.01,'margin':1.01,'calibration_answers':0,
                    'calibration_primary_precision':None,'calibration_false_accepts':0,'reason':'No feasible calibration operating point; abstain.'}
