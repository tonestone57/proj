from core.base import CognitiveModule

class VisionModule(CognitiveModule):
    def receive(self, message):
        if message["type"] == "image_input":
            processed = self.process_image(message["data"])
            self.scheduler.submit(self, {"type": "vision_output", "data": processed})

    def process_image(self, img):
        return {"features": "placeholder"}
