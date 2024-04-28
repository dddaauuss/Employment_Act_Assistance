#Importing Libraries 

import os 
import streamlit as st 
import openai
from dotenv import load_dotenv 



#Load environment var
load_dotenv()

#Initialize OpenAI client 
openai.api_key=os.getenv("OPENAI_API_KEY")

# Define function for chatbot interaction
def chatbot(message_list, user_input, work_period, notice_period, salary_description, selected_description,issue_details):
    # Append user information to the message list
    message_list.append({'role': 'system', 'content': f'Work Period: {work_period}'})
    message_list.append({'role': 'system', 'content': f'Notice Period: {notice_period}'})
    message_list.append({'role': 'system', 'content': f'Issue/Problem Details: {issue_details}'})
    message_list.append({'role': 'system', 'content': f'Selected Description: {selected_description}'})
    message_list.append({'role': 'system', 'content': f'Selected Description: {salary_description}'})
    message_list.append({'role': 'user', 'content': user_input})
    # Set up the response prompt based on the user query
    response_prompt = {
    "role": "assistant",
    "content": f'''As a legal expert on the Employment Act 1955 in Malaysia, provide a detailed explanation based on the following inputs:

        Work Period: {work_period}
        Notice Period: {notice_period}
        salary Description: {salary_description}
        Selected Description: {selected_description}
        Issue/Problem Details: {issue_details}
        User Input: {user_input}

        Your response MUST ALWAYS INCLUDE RELEVANT SECTION OF THE ACT, interpretations, and any important legal precedents.
        Additionally, consider referencing past legal cases or precedents to support your advice. For example, you can mention, "Based on past cases, individuals in similar situations have been entitled to compensation for similar issues. However, each case is unique, and it's essential to consult with a legal professional to assess your specific circumstances/Individuals entitled to compensation in lieu of the insufficient notice period."
        Your advice must aim to PROVIDE ACTIONABLE STEPS and recommendations to address the user's problem effectively. Please structure your response clearly(explain in point) and concisely to ensure the user can understand and follow the guidance provided.
    '''
}

    # Append user input to the message list
    message_list.append({'role': 'user', 'content': user_input})

    # Append the response prompt to the message list
    message_list.append(response_prompt)

    # Generate response from GPT-3.5 Turbo
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=message_list,
        temperature=0.8
    )

    # Extract assistant's response from the generated completion
    assistant_response = response.choices[0].message.content

    # Append assistant's response to the message list
    message_list.append({'role': 'assistant', 'content': assistant_response})

    return message_list, assistant_response

# Main function for streamlit app
def main():
    st.title('Employment Act Assistance for Employee')

    # Set up the initial message list with system introduction
    message_list = [{'role': 'system', 'content': 'You are a helpful and thoughtful AI assistant knowledgeable about employment laws in Malaysia.'}]

    # User Input
    with st.sidebar:
        st.subheader('User Information')
        work_period = st.text_input('Work Period', '')
        notice_period = st.text_input('Notice Period', '')
        

        # Selectbox for issue/problem description
        salary_options = ['<RM2000', '>RM2000', '<RM4000', '>RM4000']
        salary_description = st.selectbox('Salary Range:', salary_options)
    
        # Selectbox for issue/problem description
        description_options = ['Termination', 'EPF (Employee Provident Fund)', 'Accident', 'Other']
        selected_description = st.selectbox('Issue/Problem:', description_options)
    
        # Text input for additional details
        issue_details = st.text_area('Issue/Problem Description:', height=100)
    
        # If "Other" is selected, allow user to input custom description
        if selected_description == 'Other':
            user_input = st.text_area('Issue/Problem Details:', height=100)
        else:
            user_input = selected_description
            
        # Generate response button
        submit_button = st.button('Generate Response')

    # Process user input and display response
    if submit_button and user_input:
        message_list, assistant_output = chatbot(message_list, user_input, work_period, notice_period, salary_description,selected_description, issue_details)

        # Display the response
        st.header("Your generated response")
        st.write(assistant_output)

if __name__ == '__main__':
    main()