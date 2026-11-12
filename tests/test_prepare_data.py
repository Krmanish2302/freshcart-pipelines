from sklearn.datasets import load_iris
from iris_project.transformers.prepare_data import transform
from iris_project.transformers.train_model import train
from iris_project.transformers.evaluate_model import evaluate
from iris_project.data_exporters.export_metrics import export_metrics

def test_split_is_80_20():
    df = load_iris(as_frame=True).frame
    out = transform(df)
    assert (out["split"] == "train").sum() == 120
    assert (out["split"] == "test").sum() == 30

def test_custom_metrics_exporter():
    df = load_iris(as_frame=True).frame
    split_df = transform(df)
    pred_df = train(split_df, max_depth=3)
    metrics_df = evaluate(pred_df)
    exported = export_metrics(metrics_df)
    assert len(exported) == 4
    acc = exported[exported['metric'] == 'accuracy']['value'].values[0]
    assert acc >= 0.8
