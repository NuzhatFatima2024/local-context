import os
import asyncio
import openai
from pydantic import BaseModel
from connection import config
from agents import Agent,Runner,RunContextWrapper,function_tool,trace
from dotenv import load_dotenv

load_dotenv()
openai_api_key =os.getenv("OPENAI_API_KEY")
"""class UserInfo(BaseModel) :
    user_id:int|str
    name:str
    user= UserInfo(user_id =001,name = "Anam"),UserInfo(user_id = "ai",name ="iffat")"""

class BankAccount(BaseModel):
    accout_number:int|str
    name:str
    account_balance:int|float
    account_type:str


bank_account=BankAccount(
    accout_number="Pk012356980",
    name = "Fatima Khan",
    account_balance=75500.50,
    account_type="savings"

)
class StudentProfile(BaseModel):
    student_id:str|int
    student_name:str
    student_semester:str|int
    total_courses:int

student_profile=StudentProfile(
    student_id=0000,
    student_name="Hasan Ahmed",
    student_semester="4",
    total_courses=5

)

@function_tool
def get_student_info(wrapper:RunContextWrapper[StudentProfile]):
    return f"The student info is given below{wrapper.context.student_name} having id {wrapper.context.student_id}in semester{wrapper.context.student_semester} with courses{wrapper.context.total_courses}"
agent=Agent(
    name="Student_Agent",
    instructions="yyou are a student agent. your task is to call the tool and provide student info!",
    tools = [get_student_info]
)

class LibraryBook(BaseModel):
    book_id:str|int
    book_title:str
    author_name:str
    is_available:bool

library_book = LibraryBook(
    book_id="st_098",
    book_title="Python Programming",
    author_name="Smith",
    is_available=True
)

@function_tool
def get_book_info(wrapper:RunContextWrapper[LibraryBook]):
    return f"The book info is given below{wrapper.context.book_id} having title{wrapper.context.book_title} written by{wrapper.context.author_name} with availbility{wrapper.context.is_available}"
agent=Agent(
    name="Book_Agent",
    instructions="you are a book agent. your task is to call the tool and provide book info!",
    tools = [get_book_info]
)
'''@function_tool
def get_user_info(wrapper:RunContextWrapper[UserInfo]):
    return f"the user info is{wrapper.context}"
personal_agent= Agent(
    name="assistant",
    instructions="you are a helpful assistant.your task is to call tool,call the context from high to low user id",
    tools=[get_user_info]
)'''

@function_tool
def get_bank_info(wrapper:RunContextWrapper[BankAccount]):
    return f"The customer name{wrapper.context.name} having account number{wrapper.context.accout_number}with balance{wrapper.context.account_balance}"
bank_agent= Agent(
    name="Bank_Agent",
    instructions="you are a bank agent .your task is to call tool and provide info about user in local context",
    tools=[get_bank_info]
)

async def main1():
    with trace("LLM given context in local(for Bank Account)"):
        result=await Runner.run(
            bank_agent,
            "tell customer name with account id as well as account balance with context",
            run_config=config,
            context=bank_account
        )
        print("Bank Agent:",result.final_output)

async def main2():
    with trace("LLM given context in local(for StudentProfile)"):
        result=await Runner.run(
            student_profile,
            "tell student name with id as well as semester with context",
            run_config=config,
            context=student_profile
        )
        print("Student Agent:",result.final_output)


async def main3():
    with trace("LLM given context in local(with Library book info"):
        result=await Runner.run(
            library_book,
            "tell book name with author name as well as its availability with context",
            run_config=config,
            context=student_profile
        )
        print("Library Agent:",result.final_output)

if __name__=="__main__":
    asyncio.run(main1())
    asyncio.run(main2())
    asyncio.run(main3())
