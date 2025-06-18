from typing import Dict, List, Any, Optional, Union
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import logging
from dataclasses import dataclass
from datetime import datetime
from PIL import Image
import requests
from memory import ArtHistoryMemory
from tools import ArtAnalysisTools
from vision_tools import VisionAnalysisTools
from prompt_templates import PromptTemplates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentState:
    """Enhanced state for Professor Helena agent with vision capabilities"""
    messages: List[BaseMessage]
    artwork_context: Optional[Dict[str, Any]] = None
    image_analysis: Optional[Dict[str, Any]] = None
    visual_elements: Optional[Dict[str, Any]] = None
    historical_perspectives: List[Dict[str, Any]] = None
    current_analysis: Optional[str] = None
    critique_complete: bool = False
    discussion_mode: bool = False
    has_image: bool = False

class ProfessorHelena:
    """
    Enhanced Professor Helena AI Agent - Art History Expert with Vision
    Specialized in providing scholarly, methodical art analysis with historical context
    Now includes image analysis capabilities using open-source vision models
    """
    
    def __init__(self, 
                 text_model: str = "llama3.1:8b",
                 vision_model: str = "llava:13b"):  # or "llama3.2-vision:11b"
        """
        Initialize Professor Helena with vision capabilities
        
        Args:
            text_model: Ollama text model (llama3.1:8b recommended)
            vision_model: Ollama vision model (llava:13b or llama3.2-vision:11b)
        """
        # Text-only model for regular analysis
        self.text_llm = ChatOllama(
            model=text_model,
            temperature=0.7,
            top_p=0.9
        )
        
        # Vision model for image analysis
        self.vision_llm = ChatOllama(
            model=vision_model,
            temperature=0.6,  # Slightly lower for more consistent visual analysis
            top_p=0.9
        )
        
        self.memory = ArtHistoryMemory()
        self.tools = ArtAnalysisTools()
        self.vision_tools = VisionAnalysisTools()
        self.prompts = PromptTemplates()
        
        # Initialize the enhanced agent graph
        self.graph = self._create_agent_graph()
        
    def _create_agent_graph(self) -> StateGraph:
        """Create the enhanced LangGraph workflow with vision capabilities"""
        
        def process_input(state: AgentState) -> AgentState:
            """Process input and detect if image is present"""
            logger.info("Professor Helena: Processing input...")
            
            last_message = state.messages[-1] if state.messages else None
            
            # Check if message contains image
            has_image = self._detect_image_in_message(last_message)
            state.has_image = has_image
            
            if has_image:
                logger.info("Professor Helena: Image detected, preparing for visual analysis...")
            
            return state
        
        def analyze_image_content(state: AgentState) -> AgentState:
            """Analyze the visual content of the artwork image"""
            logger.info("Professor Helena: Analyzing visual content...")
            
            last_message = state.messages[-1]
            
            # Extract image from message
            image_data = self._extract_image_from_message(last_message)
            
            if image_data:
                # Comprehensive visual analysis using vision model
                visual_analysis_prompt = self.prompts.get_visual_analysis_prompt()
                
                # Create message with image for vision model
                vision_message = self._create_vision_message(visual_analysis_prompt, image_data)
                
                visual_analysis = self.vision_llm.invoke([vision_message]).content
                
                # Extract structured visual elements
                visual_elements = self.vision_tools.parse_visual_elements(visual_analysis)
                
                state.image_analysis = {
                    "raw_analysis": visual_analysis,
                    "timestamp": datetime.now().isoformat()
                }
                state.visual_elements = visual_elements
                
                logger.info("Professor Helena: Visual analysis complete")
            
            return state
            
        def analyze_artwork(state: AgentState) -> AgentState:
            """Enhanced artwork analysis incorporating visual information"""
            logger.info("Professor Helena: Beginning comprehensive artwork analysis...")
            
            last_message = state.messages[-1].content if state.messages else ""
            
            # Extract artwork information from text
            artwork_info = self.tools.extract_artwork_info(last_message)
            
            # Enhance with visual information if available
            if state.visual_elements:
                artwork_info.update({
                    "visual_analysis": state.image_analysis,
                    "formal_elements": state.visual_elements
                })
            
            # Search for relevant historical context
            search_query = self._create_enhanced_search_query(artwork_info, state.visual_elements)
            relevant_docs = self.memory.search_similar_artworks(search_query)
            
            # Generate enhanced analysis incorporating visual data
            analysis_prompt = self.prompts.get_enhanced_analysis_prompt(
                artwork_info, 
                relevant_docs,
                state.visual_elements,
                state.image_analysis
            )
            
            analysis = self.text_llm.invoke(analysis_prompt).content
            
            state.artwork_context = artwork_info
            state.current_analysis = analysis
            
            return state
            
        def generate_historical_perspectives(state: AgentState) -> AgentState:
            """Generate historical perspectives enhanced with visual understanding"""
            logger.info("Professor Helena: Generating enhanced historical perspectives...")
            
            perspectives_prompt = self.prompts.get_enhanced_perspectives_prompt(
                state.artwork_context, 
                state.current_analysis,
                state.visual_elements
            )
            
            perspectives_response = self.text_llm.invoke(perspectives_prompt).content
            perspectives = self.tools.parse_historical_perspectives(perspectives_response)
            
            state.historical_perspectives = perspectives
            return state
            
        def synthesize_critique(state: AgentState) -> AgentState:
            """Synthesize final critique incorporating all visual and contextual analysis"""
            logger.info("Professor Helena: Synthesizing comprehensive critique...")
            
            synthesis_prompt = self.prompts.get_enhanced_synthesis_prompt(
                state.artwork_context,
                state.current_analysis,
                state.historical_perspectives,
                state.visual_elements,
                state.image_analysis
            )
            
            final_critique = self.text_llm.invoke(synthesis_prompt).content
            
            # Store enhanced analysis in memory
            self.memory.store_analysis(
            artwork_info=state.artwork_context,
            analysis=final_critique,
            perspectives=state.historical_perspectives
            )
            
            state.messages.append(AIMessage(content=final_critique))
            state.critique_complete = True
            
            return state
            
        def discussion_mode_response(state: AgentState) -> AgentState:
            """Handle discussion with enhanced visual understanding"""
            logger.info("Professor Helena: Engaging in enhanced discussion mode...")
            
            last_message = state.messages[-1].content
            
            discussion_prompt = self.prompts.get_enhanced_discussion_prompt(
                last_message,
                state.artwork_context,
                state.historical_perspectives,
                state.visual_elements
            )
            
            response = self.text_llm.invoke(discussion_prompt).content
            state.messages.append(AIMessage(content=response))
            
            return state
        
        # Routing functions
        def should_analyze_image(state: AgentState) -> str:
            """Route to image analysis if image is present"""
            if state.has_image:
                return "analyze_image"
            return "analyze_artwork"
            
        def should_continue_to_artwork_analysis(state: AgentState) -> str:
            """Continue to artwork analysis after image processing"""
            return "analyze_artwork"
            
        def should_continue_to_perspectives(state: AgentState) -> str:
            """Decide whether to continue to perspectives generation"""
            if state.artwork_context and state.current_analysis:
                return "generate_perspectives"
            return "end"
            
        def should_continue_to_synthesis(state: AgentState) -> str:
            """Decide whether to continue to synthesis"""
            if state.historical_perspectives:
                return "synthesize"
            return "end"
        
        # Build the enhanced graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("process_input", process_input)
        workflow.add_node("analyze_image", analyze_image_content)
        workflow.add_node("analyze_artwork", analyze_artwork)
        workflow.add_node("generate_perspectives", generate_historical_perspectives)
        workflow.add_node("synthesize", synthesize_critique)
        workflow.add_node("discussion", discussion_mode_response)
        
        # Add edges with enhanced routing
        workflow.set_entry_point("process_input")
        
        workflow.add_conditional_edges(
            "process_input",
            should_analyze_image,
            {
                "analyze_image": "analyze_image",
                "analyze_artwork": "analyze_artwork"
            }
        )
        
        workflow.add_edge("analyze_image", "analyze_artwork")
        
        workflow.add_conditional_edges(
            "analyze_artwork",
            should_continue_to_perspectives,
            {
                "generate_perspectives": "generate_perspectives",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "generate_perspectives",
            should_continue_to_synthesis,
            {
                "synthesize": "synthesize",
                "end": END
            }
        )
        
        workflow.add_edge("synthesize", END)
        workflow.add_edge("discussion", END)
        
        return workflow.compile()
    
    def _detect_image_in_message(self, message: BaseMessage) -> bool:
        """Detect if message contains an image"""
        if not message:
            return False
            
        # Check for image in message content
        if hasattr(message, 'content'):
            if isinstance(message.content, list):
                return any(
                    hasattr(item, 'type') and item.type == 'image_url' 
                    for item in message.content
                )
            elif isinstance(message.content, str):
                # Check for base64 image data or image URLs
                return ('data:image/' in message.content or 
                       message.content.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')))
        
        return False
    
    def _extract_image_from_message(self, message: BaseMessage) -> Optional[str]:
        """Extract image data from message"""
        if not message:
            return None
            
        if hasattr(message, 'content'):
            if isinstance(message.content, list):
                for item in message.content:
                    if hasattr(item, 'type') and item.type == 'image_url':
                        return item.image_url.url
            elif isinstance(message.content, str):
                if 'data:image/' in message.content:
                    return message.content
        
        return None
    
    def _create_vision_message(self, prompt: str, image_data: str) -> HumanMessage:
        """Create a message for the vision model"""
        return HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_data}}
            ]
        )
    
    def _create_enhanced_search_query(self, artwork_info: Dict, visual_elements: Optional[Dict]) -> str:
        """Create enhanced search query incorporating visual elements"""
        query_parts = [artwork_info.get("description", "")]
        
        if visual_elements:
            # Add visual elements to search query
            if "style" in visual_elements:
                query_parts.append(f"style: {visual_elements['style']}")
            if "medium" in visual_elements:
                query_parts.append(f"medium: {visual_elements['medium']}")
            if "color_palette" in visual_elements:
                query_parts.append(f"colors: {', '.join(visual_elements['color_palette'])}")
            if "composition" in visual_elements:
                query_parts.append(f"composition: {visual_elements['composition']}")
        
        return " ".join(query_parts)
    
    async def analyze_artwork_with_image(self, 
                                       artwork_description: str, 
                                       image_path: Optional[str] = None,
                                       image_data: Optional[str] = None) -> str:
        """
        Analyze an artwork with optional image
        
        Args:
            artwork_description: Text description of the artwork
            image_path: Path to image file
            image_data: Base64 encoded image data
            
        Returns:
            Comprehensive art historical analysis with visual insights
        """
        message_content = artwork_description
        
        # Prepare message with image if provided
        if image_path or image_data:
            if image_path:
                # Pass the file path directly if your model supports it
                message_content = [
                    {"type": "text", "text": artwork_description},
                    {"type": "image_url", "image_url": {"url": image_path}}
                ]

        
        initial_state = AgentState(
            messages=[HumanMessage(content=message_content)],
            discussion_mode=False
        )
        
        result = await self.graph.ainvoke(initial_state)
        return result['messages'][-1].content
    
    async def analyze_artwork(self, artwork_description: str) -> str:
        """
        Analyze an artwork (text-only, maintains backward compatibility)
        """
        return await self.analyze_artwork_with_image(artwork_description)
    
    async def discuss_with_peer(self, peer_message: str, artwork_context: Dict[str, Any]) -> str:
        """
        Engage in discussion with another agent about an artwork
        Enhanced with visual understanding if available
        """
        discussion_state = AgentState(
            messages=[HumanMessage(content=peer_message)],
            artwork_context=artwork_context,
            discussion_mode=True
        )
        
        result = await self.graph.ainvoke(discussion_state)
        return result['messages'][-1].content
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Return enhanced information about this agent"""
        return {
            "name": "Professor Helena",
            "specialty": "Art History and Cultural Analysis with Visual Understanding",
            "personality": "Scholarly, methodical, historically-focused, visually perceptive",
            "approach": "Chronological and contextual analysis with multiple historical perspectives, enhanced by detailed visual analysis",
            "capabilities": [
                "Text-based artwork analysis",
                "Image-based visual analysis", 
                "Historical contextualization",
                "Multi-temporal perspectives",
                "Scholarly critique synthesis",
                "Cross-modal reasoning"
            ]
        }

# Usage example and model recommendations
"""
RECOMMENDED OPEN SOURCE MODELS:

1. **LLaVA 1.6 (13B)** - Best overall performance
   - Install: `ollama pull llava:13b`
   - Excellent for detailed visual analysis
   - Good reasoning capabilities

2. **Llama 3.2 Vision (11B)** - Latest from Meta
   - Install: `ollama pull llama3.2-vision:11b`
   - Strong performance, more recent
   - Better instruction following

3. **LLaVA 1.5 (7B)** - Good balance of speed/quality
   - Install: `ollama pull llava:7b`
   - Faster inference
   - Still good quality for most tasks

USAGE:
```python
# Initialize with your preferred models
helena = ProfessorHelena(
    text_model="llama3.1:8b",
    vision_model="llava:13b"  # or "llama3.2-vision:11b"
)

# Analyze with image
result = await helena.analyze_artwork_with_image(
    "Analyze this Renaissance painting",
    image_path="painting.jpg"
)
```
"""