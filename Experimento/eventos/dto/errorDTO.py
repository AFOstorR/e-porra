from flask import make_response
class ErrorResponse:
    

    def response(self,mensaje,stauts_code=404):
        
        resp=make_response({"mensaje":mensaje})
        resp.status_code=stauts_code
        return resp