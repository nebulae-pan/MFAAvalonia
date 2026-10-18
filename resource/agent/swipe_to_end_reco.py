from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import numpy as np

@AgentServer.custom_recognition("swipe_to_end_reco")
class SwipeToEndRecongition(CustomRecognition):
    pre_image = None

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        image = context.tasker.controller.cached_image

        if self.pre_image is None:
            self.pre_image = image
            return None
        
        if np.array_equal(self.pre_image, image):
            return CustomRecognition.AnalyzeResult(
                box=[0, 0, 1, 1], detail="found result"
            )
        
        self.pre_image = image
        return None