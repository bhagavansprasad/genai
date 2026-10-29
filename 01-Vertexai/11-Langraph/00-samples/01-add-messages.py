from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages

def sample_add_messages_01():
    msgs1 = [HumanMessage(content="Hello", id="1")]
    msgs2 = [AIMessage(content="Hi there!", id="2")]
    retval = add_messages(msgs1, msgs2)
    print(retval)

def sample_add_messages_02():
    msgs1 = [HumanMessage(content="Hello", id="1")]
    msgs2 = [HumanMessage(content="Hello", id="2")]
    retval = add_messages(msgs1, msgs2)
    print(retval)

def sample_add_messages_03():
    msgs1 = [HumanMessage(content="Hello", id="1")]
    msgs2 = [HumanMessage(content="How are you", id="1")]
    # msgs3 = [AIMessage(content="Hi there!", id="3")]
    retval = add_messages(msgs1, msgs2)
    print(retval)

def sample_add_messages_04():
    msgs1 = [HumanMessage(content="Hello", id="1")]
    msgs2 = [AIMessage(content="Hi there!", id="1")]
    retval = add_messages(msgs1, msgs2)
    print(retval)

def main():
    # sample_add_messages_01()
    # sample_add_messages_02()
    # sample_add_messages_03()
    # sample_add_messages_04()
    pass
        
if __name__ == "__main__":
    main()
