from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import json
from typing import Dict, Any
from pathlib import Path
import time

from utils import Utils

@AgentServer.custom_recognition("warehouse_reco")
class WarehouseRecongition(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        image = context.tasker.controller.cached_image

        # reco_detail = context.run_recognition(
        #     "RecoORC",
        #     image,
        #     {
        #         "RecoORC": {
        #             "recognition": "OCR",
        #             "only_rec": True,
        #             "roi": [583, 66, 502, 610]
        #         }
        #     }
        # )
        reco_detail = context.run_recognition(
            "RecoORC",
            image,
            {
                "RecoORC": {
                    "recognition": "OCR",
                    "only_rec": True,
                    "roi": [583, 66, 502, 610]
                }
            }
        )
        print(reco_detail)

        text = reco_detail.best_result.text
        print(text)
        times = int(reco_detail.best_result.text.split("：")[1].strip().split("/")[0])
        if times == 0:
            return None
        else:
            return CustomRecognition.AnalyzeResult(
                box=reco_detail.best_result.box, detail="found result"
            )