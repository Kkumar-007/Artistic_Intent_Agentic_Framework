import re
from typing import Dict, List, Any, Optional, Tuple
class VisionAnalysisTools:
    """
    Tools for analyzing visual elements in artwork images
    Works with open-source vision models to extract structured information
    """
    
    def __init__(self):
        self.color_names = {
            # Basic colors
            'red': [(255, 0, 0), (220, 20, 60), (178, 34, 34)],
            'blue': [(0, 0, 255), (0, 100, 200), (30, 144, 255)],
            'green': [(0, 255, 0), (34, 139, 34), (0, 128, 0)],
            'yellow': [(255, 255, 0), (255, 215, 0), (255, 165, 0)],
            'purple': [(128, 0, 128), (147, 112, 219), (138, 43, 226)],
            'orange': [(255, 165, 0), (255, 140, 0), (255, 69, 0)],
            'brown': [(165, 42, 42), (139, 69, 19), (160, 82, 45)],
            'black': [(0, 0, 0), (64, 64, 64), (128, 128, 128)],
            'white': [(255, 255, 255), (248, 248, 255), (245, 245, 245)],
            'gold': [(255, 215, 0), (218, 165, 32), (184, 134, 11)],
            'silver': [(192, 192, 192), (169, 169, 169), (211, 211, 211)]
        }
    
    def parse_visual_elements(self, visual_analysis: str) -> Dict[str, Any]:
        """
        Parse the raw visual analysis from vision model into structured elements
        
        Args:
            visual_analysis: Raw text output from vision model
            
        Returns:
            Structured dictionary of visual elements
        """
        elements = {
            'composition': self._extract_composition(visual_analysis),
            'color_palette': self._extract_colors(visual_analysis),
            'style': self._extract_style(visual_analysis),
            'medium': self._extract_medium(visual_analysis),
            'technique': self._extract_technique(visual_analysis),
            'subject_matter': self._extract_subject_matter(visual_analysis),
            'formal_elements': self._extract_formal_elements(visual_analysis),
            'lighting': self._extract_lighting(visual_analysis),
            'perspective': self._extract_perspective(visual_analysis),
            'texture': self._extract_texture(visual_analysis),
            'mood': self._extract_mood(visual_analysis)
        }
        
        return {k: v for k, v in elements.items() if v}  # Remove empty values
    
    def _extract_composition(self, text: str) -> Optional[str]:
        """Extract composition information"""
        composition_keywords = [
            'composition', 'arrangement', 'layout', 'structure',
            'triangular', 'circular', 'linear', 'diagonal', 'symmetrical', 'asymmetrical',
            'centered', 'off-center', 'rule of thirds', 'golden ratio'
        ]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in composition_keywords):
                return sentence.strip()
        
        return None
    
    def _extract_colors(self, text: str) -> List[str]:
        """Extract color information"""
        colors_found = []
        text_lower = text.lower()
        
        # Look for direct color mentions
        for color_name in self.color_names.keys():
            if color_name in text_lower:
                colors_found.append(color_name)
        
        # Look for color descriptions
        color_patterns = [
            r'(\w+)\s+(?:colored?|hued?|toned?)',
            r'(?:shades?|tones?|hues?)\s+of\s+(\w+)',
            r'(\w+)\s+palette',
            r'predominantly\s+(\w+)',
            r'rich\s+(\w+)',
            r'deep\s+(\w+)',
            r'vibrant\s+(\w+)',
            r'muted\s+(\w+)',
            r'warm\s+(\w+)',
            r'cool\s+(\w+)'
        ]
        
        for pattern in color_patterns:
            matches = re.findall(pattern, text_lower)
            colors_found.extend(matches)
        
        # Remove duplicates and common non-colors
        colors_found = list(set(colors_found))
        non_colors = ['light', 'dark', 'bright', 'pale', 'deep', 'rich', 'vibrant', 'muted', 'warm', 'cool']
        colors_found = [c for c in colors_found if c not in non_colors]
        
        return colors_found[:5]  # Return top 5 colors
    
    def _extract_style(self, text: str) -> Optional[str]:
        """Extract artistic style information"""
        style_keywords = [
            # Historical periods
            'renaissance', 'baroque', 'rococo', 'neoclassical', 'romantic', 'realist',
            'impressionist', 'post-impressionist', 'expressionist', 'cubist', 'surrealist',
            'abstract', 'modern', 'contemporary', 'medieval', 'gothic', 'byzantine',
            
            # Specific styles
            'realistic', 'abstract', 'figurative', 'geometric', 'organic',
            'minimalist', 'maximalist', 'decorative', 'ornate', 'simple',
            'classical', 'traditional', 'avant-garde', 'experimental'
        ]
        
        text_lower = text.lower()
        for keyword in style_keywords:
            if keyword in text_lower:
                # Find the sentence containing the style
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        return sentence.strip()
        
        return None
    
    def _extract_medium(self, text: str) -> Optional[str]:
        """Extract medium/material information"""
        medium_keywords = [
            'oil painting', 'oil on canvas', 'acrylic', 'watercolor', 'tempera',
            'fresco', 'pastel', 'charcoal', 'pencil', 'ink', 'gouache',
            'canvas', 'wood', 'panel', 'paper', 'silk', 'metal',
            'sculpture', 'bronze', 'marble', 'stone', 'clay', 'ceramic',
            'photograph', 'print', 'etching', 'lithograph', 'woodcut',
            'mixed media', 'collage', 'assemblage'
        ]
        
        text_lower = text.lower()
        for keyword in medium_keywords:
            if keyword in text_lower:
                return keyword
        
        return None
    
    def _extract_technique(self, text: str) -> Optional[str]:
        """Extract technique information"""
        technique_keywords = [
            'brushwork', 'brushstrokes', 'impasto', 'glazing', 'scumbling',
            'alla prima', 'wet-on-wet', 'dry brush', 'stippling', 'cross-hatching',
            'blending', 'layering', 'underpainting', 'overpainting',
            'chiaroscuro', 'sfumato', 'tenebrism', 'pointillism'
        ]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in technique_keywords):
                return sentence.strip()
        
        return None
    
    def _extract_subject_matter(self, text: str) -> List[str]:
        """Extract subject matter"""
        subject_keywords = [
            'portrait', 'landscape', 'still life', 'figure', 'nude', 'religious',
            'mythological', 'historical', 'genre scene', 'interior', 'exterior',
            'animal', 'flower', 'tree', 'building', 'architecture',
            'person', 'woman', 'man', 'child', 'group', 'crowd'
        ]
        
        subjects_found = []
        text_lower = text.lower()
        
        for keyword in subject_keywords:
            if keyword in text_lower:
                subjects_found.append(keyword)
        
        return list(set(subjects_found))
    
    def _extract_formal_elements(self, text: str) -> Dict[str, str]:
        """Extract formal elements (line, shape, form, space, etc.)"""
        elements = {}
        
        # Line
        line_keywords = ['line', 'linear', 'contour', 'outline', 'curved', 'straight', 'diagonal']
        line_info = self._find_info_by_keywords(text, line_keywords)
        if line_info:
            elements['line'] = line_info
        
        # Shape
        shape_keywords = ['shape', 'circular', 'rectangular', 'triangular', 'organic', 'geometric']
        shape_info = self._find_info_by_keywords(text, shape_keywords)
        if shape_info:
            elements['shape'] = shape_info
        
        # Form
        form_keywords = ['form', 'volume', 'mass', 'three-dimensional', '3d', 'dimensional']
        form_info = self._find_info_by_keywords(text, form_keywords)
        if form_info:
            elements['form'] = form_info
        
        # Space
        space_keywords = ['space', 'spatial', 'depth', 'foreground', 'background', 'middle ground']
        space_info = self._find_info_by_keywords(text, space_keywords)
        if space_info:
            elements['space'] = space_info
        
        return elements
    
    def _extract_lighting(self, text: str) -> Optional[str]:
        """Extract lighting information"""
        lighting_keywords = [
            'lighting', 'light', 'shadow', 'bright', 'dark', 'illuminated',
            'dramatic lighting', 'soft light', 'harsh light', 'natural light',
            'artificial light', 'backlighting', 'side lighting', 'front lighting',
            'chiaroscuro', 'tenebrism', 'luminous', 'glowing', 'radiant'
        ]
        
        return self._find_info_by_keywords(text, lighting_keywords)
    
    def _extract_perspective(self, text: str) -> Optional[str]:
        """Extract perspective information"""
        perspective_keywords = [
            'perspective', 'linear perspective', 'atmospheric perspective',
            'one-point perspective', 'two-point perspective', 'three-point perspective',
            'bird\'s eye view', 'worm\'s eye view', 'eye level', 'high angle', 'low angle',
            'vanishing point', 'horizon line', 'foreshortening'
        ]
        
        return self._find_info_by_keywords(text, perspective_keywords)
    
    def _extract_texture(self, text: str) -> Optional[str]:
        """Extract texture information"""
        texture_keywords = [
            'texture', 'textured', 'smooth', 'rough', 'coarse', 'fine',
            'grainy', 'silky', 'glossy', 'matte', 'bumpy', 'ridged',
            'fabric', 'skin', 'hair', 'fur', 'metal', 'wood grain'
        ]
        
        return self._find_info_by_keywords(text, texture_keywords)
    
    def _extract_mood(self, text: str) -> Optional[str]:
        """Extract mood/emotional content"""
        mood_keywords = [
            'mood', 'emotion', 'feeling', 'atmosphere', 'ambiance',
            'serene', 'peaceful', 'calm', 'tranquil', 'dramatic', 'intense',
            'melancholic', 'joyful', 'somber', 'mysterious', 'energetic',
            'contemplative', 'spiritual', 'romantic', 'nostalgic', 'powerful'
        ]
        
        return self._find_info_by_keywords(text, mood_keywords)
    
    def _find_info_by_keywords(self, text: str, keywords: List[str]) -> Optional[str]:
        """Helper function to find information related to specific keywords"""
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                return sentence.strip()
        return None
    
    def analyze_color_harmony(self, colors: List[str]) -> Dict[str, Any]:
        """Analyze color relationships and harmony"""
        if not colors:
            return {}
        
        analysis = {
            'dominant_colors': colors[:3],
            'color_count': len(colors),
            'color_temperature': self._assess_color_temperature(colors),
            'color_intensity': self._assess_color_intensity(colors),
            'potential_schemes': self._identify_color_schemes(colors)
        }
        
        return analysis
    
    def _assess_color_temperature(self, colors: List[str]) -> str:
        """Assess overall color temperature"""
        warm_colors = ['red', 'orange', 'yellow', 'brown', 'gold']
        cool_colors = ['blue', 'green', 'purple', 'silver']
        neutral_colors = ['black', 'white', 'gray', 'grey']
        
        warm_count = sum(1 for color in colors if color in warm_colors)
        cool_count = sum(1 for color in colors if color in cool_colors)
        
        if warm_count > cool_count:
            return 'warm'
        elif cool_count > warm_count:
            return 'cool'
        else:
            return 'balanced'
    
    def _assess_color_intensity(self, colors: List[str]) -> str:
        """Assess color intensity/saturation level"""
        # This is a simplified assessment based on color names
        high_intensity = ['red', 'blue', 'yellow', 'orange', 'purple', 'green']
        low_intensity = ['brown', 'gray', 'grey', 'beige', 'cream']
        
        high_count = sum(1 for color in colors if color in high_intensity)
        low_count = sum(1 for color in colors if color in low_intensity)
        
        if high_count > low_count:
            return 'vibrant'
        elif low_count > high_count:
            return 'muted'
        else:
            return 'mixed'
    
    def _identify_color_schemes(self, colors: List[str]) -> List[str]:
        """Identify potential color schemes"""
        schemes = []
        
        # Monochromatic (variations of same color)
        if len(set(colors)) <= 2:
            schemes.append('monochromatic')
        
        # Complementary pairs
        complementary_pairs = [
            ('red', 'green'), ('blue', 'orange'), ('yellow', 'purple')
        ]
        for pair in complementary_pairs:
            if all(color in colors for color in pair):
                schemes.append('complementary')
                break
        
        # Analogous (adjacent colors)
        analogous_groups = [
            ['red', 'orange', 'yellow'],
            ['blue', 'green', 'purple'],
            ['yellow', 'green', 'blue']
        ]
        for group in analogous_groups:
            if len([color for color in colors if color in group]) >= 2:
                schemes.append('analogous')
                break
        
        # Triadic
        triadic_sets = [
            ['red', 'blue', 'yellow'],
            ['orange', 'green', 'purple']
        ]
        for triad in triadic_sets:
            if all(color in colors for color in triad):
                schemes.append('triadic')
                break
        
        return schemes if schemes else ['custom']
    
    def create_visual_summary(self, visual_elements: Dict[str, Any]) -> str:
        """Create a concise visual summary for use in analysis"""
        summary_parts = []
        
        if visual_elements.get('style'):
            summary_parts.append(f"Style: {visual_elements['style']}")
        
        if visual_elements.get('medium'):
            summary_parts.append(f"Medium: {visual_elements['medium']}")
        
        if visual_elements.get('color_palette'):
            colors = ', '.join(visual_elements['color_palette'][:3])
            summary_parts.append(f"Primary colors: {colors}")
        
        if visual_elements.get('composition'):
            summary_parts.append(f"Composition: {visual_elements['composition'][:100]}...")
        
        if visual_elements.get('subject_matter'):
            subjects = ', '.join(visual_elements['subject_matter'][:3])
            summary_parts.append(f"Subject: {subjects}")
        
        if visual_elements.get('mood'):
            summary_parts.append(f"Mood: {visual_elements['mood']}")
        
        return ' | '.join(summary_parts)
    
    def compare_visual_elements(self, elements1: Dict[str, Any], elements2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare visual elements between two artworks"""
        comparison = {
            'similarities': [],
            'differences': [],
            'style_relationship': 'unknown'
        }
        
        # Compare colors
        colors1 = set(elements1.get('color_palette', []))
        colors2 = set(elements2.get('color_palette', []))
        common_colors = colors1.intersection(colors2)
        
        if common_colors:
            comparison['similarities'].append(f"Shared colors: {', '.join(common_colors)}")
        
        # Compare styles
        style1 = elements1.get('style', '').lower()
        style2 = elements2.get('style', '').lower()
        
        if style1 and style2:
            if style1 == style2:
                comparison['similarities'].append(f"Same style: {style1}")
                comparison['style_relationship'] = 'identical'
            elif any(word in style2 for word in style1.split()) or any(word in style1 for word in style2.split()):
                comparison['similarities'].append(f"Related styles: {style1} and {style2}")
                comparison['style_relationship'] = 'related'
            else:
                comparison['differences'].append(f"Different styles: {style1} vs {style2}")
                comparison['style_relationship'] = 'different'
        
        # Compare composition
        comp1 = elements1.get('composition', '').lower()
        comp2 = elements2.get('composition', '').lower()
        
        if comp1 and comp2:
            common_comp_words = set(comp1.split()).intersection(set(comp2.split()))
            if len(common_comp_words) > 2:  # More than just articles/prepositions
                comparison['similarities'].append("Similar compositional approaches")
            else:
                comparison['differences'].append("Different compositional approaches")
        
        return comparison
    
    def extract_technical_details(self, visual_analysis: str) -> Dict[str, Any]:
        """Extract technical painting/artistic details"""
        details = {}
        
        # Brushwork analysis
        brushwork_patterns = [
            r'brush(?:work|stroke)s?\s+(?:are|is)?\s*([^.]+)',
            r'(?:thick|thin|bold|delicate|loose|tight)\s+(?:brush|stroke)s?',
            r'impasto|glazing|scumbling|alla prima'
        ]
        
        brushwork_info = []
        for pattern in brushwork_patterns:
            matches = re.findall(pattern, visual_analysis.lower())
            brushwork_info.extend(matches)
        
        if brushwork_info:
            details['brushwork'] = ' '.join(brushwork_info[:2])
        
        # Canvas/support information
        support_keywords = ['canvas', 'wood', 'panel', 'paper', 'board', 'copper', 'silk']
        for keyword in support_keywords:
            if keyword in visual_analysis.lower():
                details['support'] = keyword
                break
        
        # Size references
        size_patterns = [
            r'(?:large|small|medium|huge|tiny|massive|miniature)\s+(?:scale|size|work|painting)',
            r'(?:monumental|intimate|grand|modest)\s+(?:scale|proportions?)'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, visual_analysis.lower())
            if match:
                details['scale'] = match.group()
                break
        
        # Condition/preservation
        condition_keywords = ['restored', 'damaged', 'pristine', 'aged', 'cracked', 'faded', 'well-preserved']
        for keyword in condition_keywords:
            if keyword in visual_analysis.lower():
                details['condition'] = keyword
                break
        
        return details