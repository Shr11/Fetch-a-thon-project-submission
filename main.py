import json
import sys
from typing import Any, Dict, List
from uagents import Agent, Bureau, Context, Model
from get_jobs import get_highest_salary, find_jobs

class Query(Model):
    name: str

class JobsData(Model):
    jobs: List[Dict[str, Any]]
    
class selecetedJob(Model):
    job_url: str
    
# Instantiating agents
searching_agent = Agent(name="shopping_agent")
job_agent = Agent(name="job_agent")
getting_job_agent = Agent(name="getting_job_agent")


@searching_agent.on_event("startup")
async def setting_up(ctx: Context):
    ctx.storage.set("completed", False)
    
@job_agent.on_message(Query, replies={Query, JobsData})
async def handle_message(ctx: Context, sender: str, msg: Query):
    print(f"JOb query recieved from {sender}")
    # Send the job data back to the searching agent
    jobs = find_jobs(msg.name)
    if len(jobs) > 0:
        await ctx.send(searching_agent.address, Query(name="Jobs found!"))
    else:
        ctx.logger.info(f"Sending no Jobs back to {sender}")
        

@getting_job_agent.on_message(Query,replies={Query})
async def handle_job_data(ctx: Context, sender: str, msg: Query):
    ctx.logger.info(f"Getting Job from data received from {sender}")
    ctx.logger.info(f"{msg.name}")
    

@searching_agent.on_message(JobsData, replies={Query})
async def handle_jobs_data(ctx: Context, sender: str, msg: JobsData):
    ctx.logger.info(f"Jobs data received from {sender}")
    ctx.storage.set("jobs", json.dumps(msg.jobs))
    
@searching_agent.on_message(selecetedJob)
async def handle_bought_product(ctx: Context, sender: str, msg: selecetedJob):
    ctx.logger.info(f"Selected job received from {sender}")
    get_selected_jobs_str = ctx.storage.get("selected_jobs") or ""
    get_selected_jobs = get_selected_jobs_str.split('|')
    get_selected_jobs.append(msg.product_url)
    ctx.storage.set("selected_jobs", '|'.join(get_selected_jobs))
    
@searching_agent.on_message(Query)
async def handle_product_data(ctx: Context, sender: str, msg: Query):
    ctx.logger.info(f"Product data received from {sender}")
    await ctx.send(getting_job_agent.address,
                   Query(name="Thanks for searching for jobs with us!"))
    ctx.storage.set("completed", True)
    

@searching_agent.on_interval(period=5, messages=Query)
async def serve_the_user(ctx: Context):
    query = sys.argv[1] if len(sys.argv) > 1 else "levis"
    completed = ctx.storage.get("completed")
    ctx.logger.info(f"Querying for {query}")
    ctx.logger.info(f"Status: {completed}")
    if (not completed):
        await ctx.send(job_agent.address, Query(name=query))
    else:
        get_selected_jobs = ctx.storage.get("selected_jobs") or ""
        ctx.logger.info('\n'.join(get_selected_jobs.split('|')))
        
bureau = Bureau()
bureau.add(getting_job_agent)
bureau.add(job_agent)
bureau.add(searching_agent)

if __name__ == "__main__":
    bureau.run()

