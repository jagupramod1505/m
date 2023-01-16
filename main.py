from fastapi import FastAPI
import routes
import uvicorn



app = FastAPI()

app.include_router(routes.router)



if __name__ == '__main__':

    uvicorn.run("main:app", host='172.16.22.6', port=8005, reload = True,debug =True)

    print("running")
