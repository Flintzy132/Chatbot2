import requests
import json
from openai import OpenAI

client = OpenAI(
    api_key='sk-svcacct-4_bjMhfrt_mQhKOaZRu2oKRhS1I6rFpO3hpz0X07d_XsnU8Q9T3BlbkFJ9Fsguw1pj0VF43EO6VWiDS2v1zWsKTvRMG6z9kqAUqyrQ_IAA'
)


def call_url(temp):
    print("done")
    # create vector store
    vector_store = client.beta.vector_stores.create(
        name="Employee Data"
    )

    my_assistant = client.beta.assistants.create(
        instructions="There are files in the vector store search for the answer within the file and just say the answer without any other word, if the answer is not present then just say that it is not available and dont give any random answer.",
        name="HR Helper",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": vector_store.id}},
        model="gpt-4o"
    )

    # transfer assistant key to the data file
    with open('assistant_key.json', 'r') as file:
        data = json.load(file)
        data['assistant_key'] = "1"

    with open('assistant_key.json', 'w') as f:
        json.dump(data, f)

    # first api data
    emp_id = temp
    url1 = "https://weatworktest.mahyco.com/webapi/api/MyProfile/GetMyProfileData"
    headers1 = {
        "Authorization": "bearer k-Fa6IAPmcfVgeTPcBhWTaYvPqhpzVaUbH38CMMSH7JHzTJknzDSO4U1M4wgiQU4IbiYpqtHdB3jK1aoi9gDbcUmUvmH4DgnlNbGsvCnkZKtLJz79KmM2C-IWSqb0FHaxseeFICkdzkN1PTPjbPY8GYIpYugJi4qgE9wqVKKXAEv75DW_ZiXVRaYJIRvTHmAPnIbSbbS91BSZXNTtACibA"}
    data1 = {"loginDetails": {
        "LoginEmpID": 97260738,
        "LoginEmpCompanyCodeNo": "4000"
    }
    }

    response1 = requests.post(url1, headers=headers1, json=data1)

    # transfer api data to api_data.json
    with open('api_data.json', 'w') as file:
        json.dump(response1.json(), file, indent=2)

    # second api data
    url = "https://weatworktest.mahyco.com/webapi/api/Leave/GetLeaveData"
    headers = {
        "Authorization": "bearer k-Fa6IAPmcfVgeTPcBhWTaYvPqhpzVaUbH38CMMSH7JHzTJknzDSO4U1M4wgiQU4IbiYpqtHdB3jK1aoi9gDbcUmUvmH4DgnlNbGsvCnkZKtLJz79KmM2C-IWSqb0FHaxseeFICkdzkN1PTPjbPY8GYIpYugJi4qgE9wqVKKXAEv75DW_ZiXVRaYJIRvTHmAPnIbSbbS91BSZXNTtACibA"}
    data = {"loginDetails": {
        "LoginEmpID": 97260738,
        "LoginEmpCompanyCodeNo": "4000",
        "LoginEmpGroupId": "4000"
    }
    }

    response = requests.post(url, headers=headers, json=data)

    # transfer api data to api_data2.json
    with open('api_data2.json', 'w') as file:
        json.dump(response.json(), file, indent=2)

    # create first file for vector
    file1 = client.files.create(
        file=open("api_data.json", "rb"),
        purpose="fine-tune"
    )

    # create second file for vector
    file2 = client.files.create(
        file=open("api_data2.json", "rb"),
        purpose="fine-tune"
    )

    # transfer files to vector store
    vector_store_file_batch = client.beta.vector_stores.file_batches.create(
        vector_store_id=vector_store.id,
        file_ids=[file1.id, file2.id]
    )
    return my_assistant.id
