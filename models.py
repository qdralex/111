class Result:
    def __init__(self, original_path, predict, date, time):
        self.original_path = original_path
        self.predict = predict
        self.date = date
        self.time = time
        
class ResultWeb:
    def __init__(self, original_img_byte, predict, date, time):
        self.original_img_byte = original_img_byte
        self.predict = predict
        self.date = date
        self.time = time