import os
import json
import google.generativeai as genai
from visual_interpreter import interpret_visual_data
from knowledge_retriever import retrieve_knowledge

# Configure Gemini API
if "GOOGLE_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def generate_marketing_consultation(original_image_path: str, heatmap_path: str) -> dict:
    """
    Orchestrates the RAG pipeline to generate a marketing consultation report.
    
    Steps:
    1. Visual Interpretation (Gemini Vision) -> Text Description
    2. Knowledge Retrieval (ChromaDB) -> Relevant Marketing Concepts
    3. Synthesis (Gemini Pro) -> Final Report
    """
    print("--- Starting Marketing AI Consultation ---")
    
    # Step 1: Visual Interpretation
    print("Step 1: Interpreting Visual Data...")
    visual_context = interpret_visual_data(original_image_path, heatmap_path)
    if visual_context.startswith("Error"):
        return {"error": visual_context}
    
    print(f"Visual Context: {visual_context[:100]}...")

    # Step 2: Knowledge Retrieval
    print("Step 2: Retrieving Marketing Knowledge...")
    # Use the visual context to find relevant theories
    knowledge_items = retrieve_knowledge(visual_context, n_results=3)
    
    knowledge_text = ""
    for item in knowledge_items:
        knowledge_text += f"- **{item['concept']}**: {item['definition']}\n  Advice: {item['advice']}\n  Case Study: {item.get('case_study', 'N/A')}\n\n"
        
    print(f"Retrieved {len(knowledge_items)} concepts.")

    # Step 3: Synthesis
    print("Step 3: Synthesizing Final Report...")
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')
        
        prompt = f"""
        You are a Senior Marketing Director and UX Psychologist.
        
        Task:
        Generate a professional marketing consultation report based on the provided user behavior analysis and marketing theories.
        
        Context (User Behavior Analysis):
        {visual_context}
        
        Relevant Marketing Theories (RAG Knowledge):
        {knowledge_text}
        
        Instructions:
        1. **Diagnosis**: Analyze the user's behavior using the provided theories. Explain WHY they behaved this way (e.g., "The user skipped the banner likely due to Banner Blindness").
        2. **Critique**: Evaluate the current design's effectiveness based on the diagnosis.
        3. **Action Plan**: Provide concrete, actionable steps to improve the design. Use the "Advice" from the marketing theories.
        4. **Tone**: Professional, insightful, and constructive. Use marketing terminology correctly.
        
        Output Format (JSON):
        {{
            "diagnosis": "Detailed diagnosis of the problem...",
            "critique": "Evaluation of the current design...",
            "action_plan": [
                "Step 1: ...",
                "Step 2: ..."
            ],
            "applied_theories": ["Theory 1", "Theory 2"]
        }}
        """
        
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
        
    except Exception as e:
        print(f"Error in consultation synthesis: {str(e)}")
        return {"error": f"Consultation failed: {str(e)}"}
