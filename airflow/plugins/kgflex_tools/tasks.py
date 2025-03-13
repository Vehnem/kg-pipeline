from airflow.models.baseoperator import BaseOperator


class ErMatchingOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        self.input = kwargs.pop("input", None)
        super().__init__(*args, **kwargs)

    def execute(self, context):
        with open("/share/result_of_"+self.task_id+".out", "a") as f:
            f.write(f"DummyOperator {self.task_id} executed\n")
        return
    
# def ER_MATCHING_WITH_PARIS():
#     return MyCustomOperator(task_id="er_matching_with_paris")
