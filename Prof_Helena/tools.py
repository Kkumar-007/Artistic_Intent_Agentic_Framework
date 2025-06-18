import re
from typing import Dict, Any, List

class ArtAnalysisTools:
    """
    Tools for Professor Helena's art analysis capabilities
    Enhanced with robust pattern matching and period identification
    """
    
    def __init__(self):
        # Enhanced art periods with overlapping handling and styles
        self.art_periods = {
            "ancient": {
                "start": -3000, "end": 500,
                "styles": ["egyptian", "greek", "roman", "byzantine"],
                "confidence_zones": [(-3000, 500)]
            },
            "medieval": {
                "start": 500, "end": 1400,
                "styles": ["romanesque", "gothic", "illuminated", "byzantine"],
                "confidence_zones": [(500, 1000), (1000, 1400)]
            },
            "renaissance": {
                "start": 1400, "end": 1600,
                "styles": ["renaissance", "quattrocento", "cinquecento", "mannerist"],
                "confidence_zones": [(1400, 1520), (1520, 1600)]
            },
            "baroque": {
                "start": 1600, "end": 1750,
                "styles": ["baroque", "rococo", "counter-reformation"],
                "confidence_zones": [(1600, 1700), (1700, 1750)]
            },
            "neoclassical": {
                "start": 1750, "end": 1820,
                "styles": ["neoclassical", "neoclassicism", "classical revival"],
                "confidence_zones": [(1750, 1820)]
            },
            "romantic": {
                "start": 1800, "end": 1850,
                "styles": ["romantic", "romanticism", "sublime"],
                "confidence_zones": [(1800, 1850)]
            },
            "realist": {
                "start": 1850, "end": 1880,
                "styles": ["realist", "naturalist", "plein air"],
                "confidence_zones": [(1850, 1880)]
            },
            "impressionist": {
                "start": 1860, "end": 1890,
                "styles": ["impressionist", "impressionism", "plein air"],
                "confidence_zones": [(1860, 1890)]
            },
            "post-impressionist": {
                "start": 1880, "end": 1910,
                "styles": ["post-impressionist", "symbolist", "fauve"],
                "confidence_zones": [(1880, 1910)]
            },
            "modern": {
                "start": 1900, "end": 1945,
                "styles": ["cubist", "futurist", "dadaist", "surrealist", "expressionist", "abstract"],
                "confidence_zones": [(1900, 1920), (1920, 1945)]
            },
            "contemporary": {
                "start": 1945, "end": 2024,
                "styles": ["abstract expressionist", "pop art", "minimalist", "conceptual", "postmodern"],
                "confidence_zones": [(1945, 1980), (1980, 2024)]
            }
        }
        
        # Emotion synonyms for fuzzy matching
        self.emotion_synonyms = {
            "joy": ["happiness", "delight", "cheerful", "jubilant", "elated"],
            "sorrow": ["sadness", "grief", "melancholy", "mourning", "lament"],
            "anger": ["rage", "fury", "wrath", "indignation", "ire"],
            "peace": ["serenity", "tranquility", "calm", "harmony", "stillness"],
            "tension": ["anxiety", "unease", "stress", "conflict", "strain"],
            "triumph": ["victory", "success", "achievement", "glory", "conquest"],
            "despair": ["hopelessness", "anguish", "despondency", "dejection"],
            "hope": ["optimism", "aspiration", "faith", "expectation", "promise"],
            "fear": ["terror", "dread", "anxiety", "apprehension", "panic"],
            "love": ["affection", "devotion", "passion", "adoration", "tenderness"]
        }
        
        # Color synonyms for better matching
        self.color_synonyms = {
            "red": ["crimson", "scarlet", "vermillion", "cherry", "ruby", "rose"],
            "blue": ["azure", "navy", "cobalt", "cerulean", "sapphire", "turquoise"],
            "green": ["emerald", "jade", "olive", "forest", "mint", "lime"],
            "yellow": ["gold", "amber", "lemon", "canary", "ochre", "saffron"],
            "purple": ["violet", "lavender", "plum", "magenta", "amethyst"],
            "orange": ["amber", "copper", "rust", "peach", "coral", "tangerine"],
            "brown": ["bronze", "mahogany", "umber", "sienna", "chestnut"],
            "black": ["ebony", "obsidian", "charcoal", "jet", "onyx"],
            "white": ["ivory", "pearl", "cream", "alabaster", "snow"],
            "gray": ["silver", "ash", "slate", "pewter", "charcoal"]
        }
        
    def extract_artwork_info(self, description: str) -> Dict[str, Any]:
        """
        Extract key information from artwork description
        
        Args:
            description: Natural language description of artwork
            
        Returns:
            Structured artwork information
        """
        if isinstance(description, list):
        # If list of Document objects
            if description and hasattr(description[0], "page_content"):
                description = " ".join([doc.page_content for doc in description])
            else:
                description = " ".join(map(str, description))
        artwork_info = {
            "description": description,
            "title": None,
            "artist": None,
            "period": None,
            "year": None,
            "medium": None,
            "style": None,
            "subjects": [],
            "techniques": [],
            "colors": [],
            "emotions": []
        }
        
        # Extract title (look for quoted text or "titled" patterns)
        title_patterns = [
            r'"([^"]+)"',
            r"titled\s+['\"]([^'\"]+)['\"]",
            r"called\s+['\"]([^'\"]+)['\"]",
            r"painting\s+['\"]([^'\"]+)['\"]"
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                artwork_info["title"] = match.group(1)
                break
        
        # Extract artist name with more specific patterns to avoid false positives
        artist_patterns = [
            r"(?:painted|created|made|drawn|sculpted|designed)\s+by\s+([A-Z][a-z]+(?:\s+(?:van|de|da|del|du|le|la|von|di)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"artist\s+([A-Z][a-z]+(?:\s+(?:van|de|da|del|du|le|la|von|di)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"work\s+(?:of|by)\s+([A-Z][a-z]+(?:\s+(?:van|de|da|del|du|le|la|von|di)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"(?:master|painter)\s+([A-Z][a-z]+(?:\s+(?:van|de|da|del|du|le|la|von|di)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
        ]
        
        for pattern in artist_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                # Additional validation to avoid place names
                candidate = match.group(1).strip()
                # Exclude common place name patterns
                if not re.match(r'^(?:New|North|South|East|West|Saint|San|Santa)\s+', candidate, re.IGNORECASE):
                    artwork_info["artist"] = candidate
                    break
        
        # Extract year/period with multiple candidate support
        year_matches = re.findall(r"\b(1[4-9]\d{2}|20[0-2]\d)\b", description)
        if year_matches:
            # Take the first reasonable year found
            artwork_info["year"] = int(year_matches[0])
            artwork_info["periods"] = self._determine_periods_with_confidence(artwork_info["year"])
            # Set primary period as the one with highest confidence
            if artwork_info["periods"]:
                artwork_info["period"] = artwork_info["periods"][0]["period"]
        
        # Also check for period names directly mentioned
        detected_periods = self._detect_periods_from_text(description)
        if detected_periods and not artwork_info.get("period"):
            artwork_info["period"] = detected_periods[0]
            artwork_info["periods"] = [{"period": p, "confidence": 0.8} for p in detected_periods]
        
        # Extract medium
        mediums = ["oil", "watercolor", "acrylic", "tempera", "fresco", "canvas", "panel", "sculpture", "bronze", "marble"]
        for medium in mediums:
            if medium in description.lower():
                artwork_info["medium"] = medium
                break
        
        # Extract style/movement
        styles = ["renaissance", "baroque", "impressionist", "cubist", "abstract", "realistic", "surreal", "expressionist"]
        for style in styles:
            if style in description.lower():
                artwork_info["style"] = style
                break
        
        # Extract colors with fuzzy matching and synonyms
        found_colors = self._extract_colors_fuzzy(description)
        artwork_info["colors"] = found_colors
        
        # Extract emotional content with fuzzy matching
        found_emotions = self._extract_emotions_fuzzy(description)
        artwork_info["emotions"] = found_emotions
        
        return artwork_info
    
    def _determine_periods_with_confidence(self, year: int) -> List[Dict[str, Any]]:
        """
        Determine art historical periods with confidence scores for overlapping periods
        
        Args:
            year: Year of the artwork
            
        Returns:
            List of periods with confidence scores, sorted by confidence
        """
        candidates = []
        
        for period, info in self.art_periods.items():
            # Check if year falls within any confidence zone
            for zone_start, zone_end in info["confidence_zones"]:
                if zone_start <= year <= zone_end:
                    # Calculate confidence based on position within zone
                    zone_center = (zone_start + zone_end) / 2
                    zone_width = zone_end - zone_start
                    distance_from_center = abs(year - zone_center)
                    confidence = max(0.5, 1.0 - (distance_from_center / (zone_width / 2)) * 0.5)
                    
                    candidates.append({
                        "period": period,
                        "confidence": confidence,
                        "zone": f"{zone_start}-{zone_end}"
                    })
                    break
        
        # Sort by confidence (highest first)
        candidates.sort(key=lambda x: x["confidence"], reverse=True)
        return candidates
    
    def _detect_periods_from_text(self, text: str) -> List[str]:
        """Detect period names directly mentioned in text"""
        detected = []
        text_lower = text.lower()
        
        for period, info in self.art_periods.items():
            # Check period name
            if period in text_lower:
                detected.append(period)
            
            # Check associated styles
            for style in info["styles"]:
                if style in text_lower:
                    detected.append(period)
                    break
        
        return list(set(detected))  # Remove duplicates
    
    def _extract_colors_fuzzy(self, text: str) -> List[str]:
        """Extract colors using fuzzy matching with synonyms"""
        found_colors = []
        text_lower = text.lower()
        
        for base_color, synonyms in self.color_synonyms.items():
            # Check base color
            if re.search(r'\b' + base_color + r'\b', text_lower):
                found_colors.append(base_color)
            else:
                # Check synonyms
                for synonym in synonyms:
                    if re.search(r'\b' + synonym + r'\b', text_lower):
                        found_colors.append(base_color)
                        break
        
        return list(set(found_colors))  # Remove duplicates
    
    def _extract_emotions_fuzzy(self, text: str) -> List[str]:
        """Extract emotions using fuzzy matching with synonyms"""
        found_emotions = []
        text_lower = text.lower()
        
        for base_emotion, synonyms in self.emotion_synonyms.items():
            # Check base emotion
            if re.search(r'\b' + base_emotion + r'\b', text_lower):
                found_emotions.append(base_emotion)
            else:
                # Check synonyms
                for synonym in synonyms:
                    if re.search(r'\b' + synonym + r'\b', text_lower):
                        found_emotions.append(base_emotion)
                        break
        
        return list(set(found_emotions))  # Remove duplicates
    
    def parse_historical_perspectives(self, perspectives_text: str) -> List[Dict[str, Any]]:
        """
        Parse the LLM output for historical perspectives with enhanced segmentation
        
        Args:
            perspectives_text: Raw text containing multiple historical perspectives
            
        Returns:
            List of structured perspective objects
        """
        perspectives = []
        
        # Enhanced splitting patterns for various formats
        splitting_patterns = [
            r'\n(?=\d+\.\s)',  # Numbered lists: "1. ", "2. "
            r'\n(?=\*\*[^*]+\*\*)',  # Bold headers: **Header**
            r'\n(?=#{1,3}\s)',  # Markdown headers: # ## ###
            r'\n(?=[A-Z][^:]*:)',  # Colon headers: "Period Name:"
            r'\n(?=\*\s)',  # Bullet points: "* "
            r'\n(?=-\s)',  # Dash points: "- "
            r'\n(?=•\s)'   # Bullet points: "• "
        ]
        
        # Try different splitting approaches
        sections = [perspectives_text]  # Start with full text
        
        for pattern in splitting_patterns:
            new_sections = []
            for section in sections:
                split_result = re.split(pattern, section)
                if len(split_result) > 1:
                    new_sections.extend([s.strip() for s in split_result if s.strip()])
                else:
                    new_sections.append(section)
            if len(new_sections) > len(sections):
                sections = new_sections
                break
        
        for section in sections:
            if len(section.strip()) < 50:  # Skip very short sections
                continue
                
            perspective = {
                "period": "Unknown",
                "viewpoint": section.strip(),
                "key_aspects": [],
                "context": "",
                "confidence": 0.7
            }
            
            # Enhanced period detection with more patterns
            period_patterns = [
                r'(?:^|\n|\*\*|##)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:Era|Period|Century|Perspective|View|Analysis|Interpretation)',
                r'(?:Renaissance|Baroque|Medieval|Ancient|Modern|Contemporary|Impressionist|Romantic|Neoclassical|Gothic|Classical|Victorian|Enlightenment)',
                r'(\d{2}th|\d{1}st|\d{2}nd|\d{2}rd)\s+[Cc]entury',
                r'(Early|Mid|Late)\s+(Renaissance|Baroque|Medieval|Modern|Contemporary)',
                r'(Pre-|Post-)?([A-Z][a-z]+(?:ist|ism|al))'
            ]
            
            for pattern in period_patterns:
                match = re.search(pattern, section, re.IGNORECASE | re.MULTILINE)
                if match:
                    if len(match.groups()) == 1:
                        period_candidate = match.group(1).title()
                    else:
                        # Handle multi-group matches
                        period_candidate = ' '.join([g for g in match.groups() if g]).title()
                    
                    # Validate against known periods
                    period_lower = period_candidate.lower()
                    for known_period in self.art_periods.keys():
                        if known_period in period_lower or period_lower in known_period:
                            perspective["period"] = known_period.title()
                            perspective["confidence"] = 0.9
                            break
                    
                    if perspective["period"] == "Unknown":
                        perspective["period"] = period_candidate
                        perspective["confidence"] = 0.6
                    break
            
            # Extract key aspects with more flexible patterns
            aspect_patterns = [
                r'[-•*]\s*([^\n]+)',  # Bullet points
                r'\d+\.\s*([^\n]+)',  # Numbered lists
                r'(?:Key|Important|Notable|Significant)\s+(?:aspects?|points?|elements?):\s*([^\n]+)',
                r'(?:They would|This period|Scholars)\s+(?:emphasize|focus on|highlight|note)\s+([^.]+)'
            ]
            
            for pattern in aspect_patterns:
                matches = re.findall(pattern, section, re.IGNORECASE)
                if matches:
                    perspective["key_aspects"].extend(matches[:3])  # Limit to top 3
                    break
            
            # If no aspects found, extract from main text
            if not perspective["key_aspects"]:
                sentences = re.split(r'[.!?]+', section)
                key_sentences = [s.strip() for s in sentences if 20 < len(s.strip()) < 150][:2]
                perspective["key_aspects"] = key_sentences
            
            perspectives.append(perspective)
        
        # Sort by confidence and limit to 5 perspectives
        perspectives.sort(key=lambda x: x["confidence"], reverse=True)
        return perspectives[:5]
    
    def identify_artistic_elements(self, description: str) -> Dict[str, List[str]]:
        """
        Identify formal artistic elements in the description
        
        Returns:
            Dictionary categorizing artistic elements
        """
        elements = {
            "composition": [],
            "color": [],
            "line": [],
            "form": [],
            "texture": [],
            "light": [],
            "space": []
        }
        
        # Composition terms
        comp_terms = ["balanced", "symmetrical", "asymmetrical", "diagonal", "triangular", "circular", "vertical", "horizontal"]
        elements["composition"] = [term for term in comp_terms if term in description.lower()]
        
        # Color terms
        color_terms = ["warm", "cool", "saturated", "muted", "bright", "dark", "monochromatic", "complementary"]
        elements["color"] = [term for term in color_terms if term in description.lower()]
        
        # Line terms
        line_terms = ["curved", "straight", "flowing", "rigid", "dynamic", "static", "bold", "delicate"]
        elements["line"] = [term for term in line_terms if term in description.lower()]
        
        # Form terms
        form_terms = ["three-dimensional", "flat", "sculptural", "geometric", "organic", "angular", "rounded"]
        elements["form"] = [term for term in form_terms if term in description.lower()]
        
        # Light terms
        light_terms = ["chiaroscuro", "dramatic", "soft", "harsh", "natural", "artificial", "backlighting", "spotlight"]
        elements["light"] = [term for term in light_terms if term in description.lower()]
        
        return elements