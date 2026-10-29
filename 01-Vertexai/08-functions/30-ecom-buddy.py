import time
import psycopg2  # For PostgreSQL interaction
import streamlit as st
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool

# --- Database Credentials (Store securely, e.g., environment variables) ---
PG_HOST = "127.0.0.1"
PG_DATABASE = "ecommate"
PG_USER = "dataworkx"
PG_PASSWORD = "jnjnuh"

# --- Function Declarations (Tooling) ---
def create_function_declarations():
    # ... (list_datasets and get_table functions are not relevant for PostgreSQL)
    list_tables_func = FunctionDeclaration(
        name="list_tables",
        description="List tables in the PostgreSQL database.",
        parameters={"type": "object", "properties": {}},  # No dataset_id needed
    )

    sql_query_func = FunctionDeclaration(
        name="sql_query",
        description="Get information from data in PostgreSQL using SQL queries",
        parameters={
            "type": "object",
            "properties": {"query": {"type": "string", "description": "SQL query on a single line."}},
            "required": ["query"],
        },
    )
    return [list_tables_func, sql_query_func] #Removed list_datasets and get_table


# --- PostgreSQL Interaction Functions (Tooling) ---
def execute_postgres_function(conn, function_name, params):
    if function_name == "list_tables":
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';") #Adjust schema as needed
            tables = [row[0] for row in cursor.fetchall()]
            return str(tables)
        except Exception as e:
            return f"Error listing tables: {e}"

    elif function_name == "sql_query":
        try:
            cursor = conn.cursor()
            cursor.execute(params["query"])
            results = cursor.fetchall()
            # Convert results to a list of dictionaries for easier handling
            column_names = [desc[0] for desc in cursor.description]
            results_list = [dict(zip(column_names, row)) for row in results]
            return str(results_list)
        except psycopg2.Error as e:  # Catch PostgreSQL-specific exceptions
            return f"Error executing query: {e}"
    return None

# --- Gemini Interaction Function (Tooling) ---
def call_gemini_function(model, prompt):
    chat = model.start_chat()
    prompt += """ Please give a concise, high-level summary followed by detail in plain language about where the information in your response is coming from in the database. Only use information that you learn from BigQuery, do not make up information."""
    response = chat.send_message(prompt)
    return response.candidates[0].content.parts[0]

def process_gemini_response(conn, model, response, message_placeholder): #Added conn
    api_requests_and_responses = []
    backend_details = ""
    function_calling_in_process = True
    while function_calling_in_process:
        try:
            params = {key: value for key, value in response.function_call.args.items()}
            api_response = execute_postgres_function(conn, response.function_call.name, params) #Use postgres function
            api_requests_and_responses.append([response.function_call.name, params, api_response])
            print(f"Function: {response.function_call.name}, Params: {params}, Response: {api_response}") # Debugging
            response = call_gemini_function(model, Part.from_function_response(name=response.function_call.name, response={"content": api_response}))
            backend_details += format_backend_details(api_requests_and_responses[-1])
            with message_placeholder.container():
                st.markdown(backend_details)

        except AttributeError:
            function_calling_in_process = False
    return response.text, backend_details, api_requests_and_responses

def format_backend_details(request_response):
    name, params, api_response = request_response
    details = f"- Function call:\n"
    details += f"  - Function name: ```{name}```\n\n"
    details += f"  - Function parameters: ```{params}```\n\n"
    details += f"  - API response: ```{api_response}```\n\n"
    return details


# --- Streamlit UI Functions ---
def create_streamlit_ui():
    st.set_page_config(page_title="SQL Talk with PGSql", page_icon="vertex-ai.png", layout="wide")
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("SQL Talk with PGSql")
    with col2:
        st.image("vertex-ai.png")

    st.subheader("Powered by Function Calling in Gemini")
    # ... (rest of the UI code remains the same)

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"].replace("$", r"\$"))
            try:
                with st.expander("Function calls, parameters, and responses"):
                    st.markdown(message["backend_details"])
            except KeyError:
                pass

def handle_user_input(conn, model): #Added conn
    if prompt := st.chat_input("Ask me about information in the database..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                response = call_gemini_function(model, prompt)
                full_response, backend_details, api_requests_and_responses = process_gemini_response(conn, model, response, message_placeholder) #Added conn
                st.markdown(full_response.replace("$", r"\$"))
                with st.expander("Function calls, parameters, and responses:"):
                    st.markdown(backend_details)

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response, "backend_details": backend_details}
                )

            except Exception as e:
                error_message = f"Something went wrong: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})


# --- Main execution block ---
def main():
    function_declarations = create_function_declarations()
    sql_query_tool = Tool(function_declarations=function_declarations)
    model = GenerativeModel("gemini-1.5-pro", generation_config={"temperature": 0}, tools=[sql_query_tool])

    try:
        conn = psycopg2.connect(host=PG_HOST, database=PG_DATABASE, user=PG_USER, password=PG_PASSWORD) #Postgres connection
    except psycopg2.Error as e:
        st.error(f"Database connection error: {e}")
        st.stop()  # Stop execution if connection fails

    create_streamlit_ui()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    display_chat_messages()
    handle_user_input(conn, model) #Added conn

    if 'conn' in locals(): #check if connection is established before closing it
        conn.close() #Close connection after use
    
if __name__ == "__main__":
    main()