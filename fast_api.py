from fastapi import FastAPI 
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change to specific domains in production!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

fileName = 'fast_api.json'

class AddVideo(BaseModel):
    name : str
    time : str
    
class UpdateVideo(BaseModel):
    id : int
    name : str
    time : str
    
class DeleteVideo(BaseModel):
    id : int
    
def load():
    try:
        with open(fileName , 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save(data):
    
    with open(fileName , 'w') as file:
        json.dump(data , file )
        
def reassign_ids(data):
    for index, item in enumerate(data):
        item["id"] = index + 1
    save(data)
        
        
data = load()



            # get for get data into server
            
@app.get('/listdata')
def list_data():
    result = []
    for  id , video in enumerate(data , start=1):
        result.append({"id" : id ,"name" : video["name"], "time" : video["time"] })
    return result
        
        # post for create new resources in server

@app.post('/addvideo' )
def add_video(video:AddVideo):
    name = video.name
    time = video.time
    
    result = {
        "id" : len(data) + 1,
        "name" : name,
        "time" : time
    }
    
    data.append(result)
    save(data)
    return {"message": "Video added successfully"}
   

    
    # put for rplace od pdate a full resouces 
    # patch is to update a partially part of the resources

@app.put('/updatevideo')

def update_video(video : UpdateVideo ):
    time.sleep()    # for delay in response
    id = video.id
    newname = video.name
    newtime = video.time
    
    for i in data:
        if i['id'] == id:
            i["name"] = newname
            i["time"] = newtime
            save(data)
            return {"name" : newname ,"time" : newtime ,"id" : id}
            # return {"message": "Video updated successfully"}
    return {"error": "Video not found"}

        # delete for deleting the resources in server
            
@app.delete('/deletevideo')
def delete_video(video : DeleteVideo ):
    id = video.id
    
    for i in data:
        if i["id"] == id:
            data.remove(i)
            reassign_ids(data)
            return {"message": "Video deleted successfully"}
    return {"error": "Video not found"}
    