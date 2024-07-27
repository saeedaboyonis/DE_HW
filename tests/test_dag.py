import pytest
from airflow.models import DagBag


def test_dag_loading():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id="de_hw_dag")
    assert dag is not None
    assert len(dag.tasks) > 0
