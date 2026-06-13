"""Memory management tools for the Strands Agent.

Provides save, search, and delete operations on the ChromaDB memory collection.
Each tool is decorated with @tool so the Strands Agent can invoke it automatically.
"""

import uuid
from strands import tool
from rag.vectordb import memory_collection


@tool
def save_memory(text: str, category: str = "general") -> str:
    """Save an important piece of information about the user to long-term memory.

    Use this tool whenever the user shares personal facts, preferences, skills,
    goals, or any information worth remembering for future conversations.

    Args:
        text: The information to save. Should be a clear, concise fact.
        category: The category of the memory. One of: personal, skill, preference, goal, general.
    """
    memory_id = str(uuid.uuid4())
    memory_collection.add(
        documents=[text],
        metadatas=[{"category": category}],
        ids=[memory_id],
    )
    return f"Memory saved successfully (id: {memory_id}): {text}"


@tool
def search_memory(query: str) -> str:
    """Search the user's long-term memory for relevant information.

    Use this tool before answering personalized questions to retrieve context
    about the user such as their name, skills, preferences, or goals.

    Args:
        query: The search query describing what information to look for.
    """
    count = memory_collection.count()
    if count == 0:
        return "No memories found. The memory is empty."

    n_results = min(5, count)
    results = memory_collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    if not results["documents"] or not results["documents"][0]:
        return "No relevant memories found."

    memories = []
    for doc, meta, mid in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["ids"][0],
    ):
        memories.append(f"- [{meta.get('category', 'general')}] {doc} (id: {mid})")

    return "Found memories:\n" + "\n".join(memories)


@tool
def delete_memory(memory_id: str) -> str:
    """Delete a specific memory by its ID.

    Use this when the user asks you to forget something or when information
    is outdated and needs to be removed.

    Args:
        memory_id: The unique ID of the memory to delete.
    """
    try:
        memory_collection.delete(ids=[memory_id])
        return f"Memory {memory_id} deleted successfully."
    except Exception as e:
        return f"Error deleting memory: {str(e)}"
