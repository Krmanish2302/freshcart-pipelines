import pandas as pd

try:
    if 'data_exporter' not in globals():
        from mage_ai.data_preparation.decorators import data_exporter
    if 'test' not in globals():
        from mage_ai.data_preparation.decorators import test
except ImportError:
    def data_exporter(fn):
        return fn
    def test(fn):
        return fn


@data_exporter
def export_metrics(metrics, *args, **kwargs):
    metrics.to_csv('iris_metrics.csv', index=False)
    print('Exported', len(metrics), 'evaluation metrics to iris_metrics.csv')
    return metrics


@test
def test_metrics_integrity(output, *args):
    assert len(output) == 4, 'Metrics table must have exactly 4 rows'
    assert 'metric' in output.columns and 'value' in output.columns, 'Missing metric/value columns'
    acc = output[output['metric'] == 'accuracy']['value'].values[0]
    assert acc >= 0.8, 'Exported model accuracy below minimum threshold'
