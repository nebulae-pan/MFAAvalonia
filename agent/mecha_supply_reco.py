from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import json
from typing import Dict, Any

from utils import Utils


@AgentServer.custom_recognition("mecha_supply_reco")
class StarMechaSupplyRecognition(CustomRecognition):
    config = {"特级·供货委托":"High", "加急·供货委托":"Medium", "常规·供货委托":"Low"}

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        success = False
        for key, value in self.config.items():
            if self.recognize_all_supply_level(context, argv, key, value):
                success = True
                break
        
        if not success:
            print("is not mecha supply")
            return None

        reco_detail = context.run_recognition(
            "StartMissionOCR",
            argv.image,
            {
                "StartMissionOCR": {
                    "recognition": "TemplateMatch",
                    "template": "ash_mission\\send_to_start_ash_mission.png",
                }
            }
        ) 

        return CustomRecognition.AnalyzeResult(
            box=reco_detail.best_result.box, detail="6"
        )



    def recognize_all_supply_level(self, context: Context, argv: CustomRecognition.AnalyzeArg, level:str, name: str) -> bool:
        print(level)
        reco_detail = context.run_recognition(
            "LevelOCR",
            argv.image,
            {
                "LevelOCR": {
                    "recognition": "OCR",
                    "expected": f"{level}*",
                    "threshold": 0.98,
                    "roi": [9, 47, 427, 121]
                }
            }
        )
        if reco_detail == None or reco_detail.best_result == None:
            print(f"not {level}, check next level")
            return False
        
        print(f"found {level}, click {name}")
        reco_detail = context.run_recognition(
            f"{name}MissionOCR",
            argv.image
        )
        if reco_detail == None:
            print(f"not {name}, skip {level}. (should not happen)")
            return False

        company_box = reco_detail.best_result.box
        click_job = context.tasker.controller.post_click(*Utils.random_point_in_rect(company_box))
        click_job.wait()
        print(f"click {name} success")
        return True
