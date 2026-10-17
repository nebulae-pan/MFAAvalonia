from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from maa.define import RecognitionDetail
import json
from typing import Dict, Any
from pathlib import Path
import time
from datetime import datetime

from utils import Utils

@AgentServer.custom_recognition("daily_tasks_reco")
class DailyTasksRecongition(CustomRecognition):
    config = Utils.load_json("./resource/agent/settings/daily_task_pipeline_mapping.json")
    unfinished_tasks_notion = "前往"

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        reco_detail = context.run_recognition(
            "RecoORC",
            argv.image,
            {
                "RecoORC": {
                    "recognition": "OCR",
                    "expected": f"{self.unfinished_tasks_notion}",
                    "threshold": 0.99,
                    "roi": [0, 0, 0, 0]
                }
            }
        )

        if (reco_detail == None):
            print("all tasks should be done...")
            return None

        for result in reco_detail.all_results:
            if(self.unfinished_tasks_notion not in result.text):
                continue
            self.process_daily_tasks_result(context, argv, result)



        # reco_detail = context.run_recognition(
        #     "RecoORC",
        #     argv.image,
        #     {
        #         "RecoORC": {
        #             "recognition": "OCR",
        #             "only_rec": True,
        #             "roi": [1091, 15, 182, 50]
        #         }
        #     }
        # )

        # text = reco_detail.all_results[0].text
        # print(f'ocr result: {text}')
        # current_energy = 0
        # if(text.isdigit()):
        #     current_energy = int(text) / 1000 
        # else:
        #     current_energy = int(text.split("/")[0])
        # print(f'current energy: {current_energy}')

        return CustomRecognition.AnalyzeResult(
            box=reco_detail.best_result.box, detail=reco_detail.best_result.text
        )


    roi_start_x = 540
    roi_height = 50
    def process_daily_tasks_result(self, context: Context, argv: CustomRecognition.AnalyzeArg, result: RecognitionDetail):
        new_roi = [
            self.roi_start_x,
            result.box[1] - self.roi_height,
            result.box[0] - self.roi_start_x,
            self.roi_height
        ]
        reco_detail = context.run_recognition(
            "taskORC",
            argv.image,
            {
                "taskORC": {
                    "recognition": "OCR",
                    "only_rec": True,
                    "roi": new_roi
                }
            }
        ) 
        if(reco_detail == None):
            print(f"found task item detail failed in {new_roi}...")
            return
        task_detail = reco_detail.all_results[0].text

        print(f"auto complete task...")

        for key, value in self.config.items():
            if(key not in task_detail):
                continue
            print(f"found task {key} in {task_detail}...")
            time_limit = value.get('time_limit')
            if time_limit is not None and self.is_before_time(time_limit):
                print(f"Current time is before time limit {time_limit}, skipping task")
                continue
            click_job = context.tasker.controller.post_click(*Utils.random_point_in_rect(result.box))
            click_job.wait()
            time.sleep(1)
            print(f"run task {value['task']}...")
            context.run_task(value['task'], value['pipeline_override'])
            break



    def test_roi(self, context: Context, argv: CustomRecognition.AnalyzeArg, box: list[int]):
        reco_detail = context.run_recognition(
            "RecoORC",
            argv.image,
            {
                "RecoORC": {
                    "recognition": "OCR",
                    "only_rec": True,
                    "roi": box
                }
            }
        ) 
        print(reco_detail.all_results)


    def is_before_time(self, target_time: str) -> bool:
        """
        Compare current time with target time in HH:mm:ss format
        Returns True if current time is before target time
        """
        current_time = datetime.now().strftime("%H:%M:%S")
        return current_time < target_time