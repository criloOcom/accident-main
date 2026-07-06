"""Zone extraction module for legal decisions."""

from typing import Optional


def extract_zones(decision: dict) -> dict:
    """
    Extract structured zones from a legal decision.
    
    Args:
        decision: Decision dictionary with 'text' and 'zones' fields
    
    Returns:
        Dictionary with extracted zones
    """
    zones = {
        "introduction": "",
        "expose": "",
        "moyens": "",
        "motivations": "",
        "dispositif": "",
        "annexes": ""
    }
    
    text = decision.get("text", "")
    zone_data = decision.get("zones", {})
    
    for zone_name, segments in zone_data.items():
        if zone_name in zones and segments:
            # Sort segments by start position
            sorted_segments = sorted(segments, key=lambda x: x.get("start", 0))
            # Extract and concatenate segments
            zones[zone_name] = "".join(
                text[seg["start"]:seg["end"]]
                for seg in sorted_segments
                if seg.get("start") is not None and seg.get("end") is not None
            )
    
    return zones


def format_zones_for_display(zones: dict) -> str:
    """
    Format extracted zones for human-readable display.
    
    Args:
        zones: Dictionary with extracted zones
    
    Returns:
        Formatted string
    """
    parts = []
    
    zone_labels = {
        "introduction": "INTRODUCTION",
        "expose": "EXPOSÉ DU LITIGE",
        "moyens": "MOYENS",
        "motivations": "MOTIVATIONS",
        "dispositif": "DISPOSITIF",
        "annexes": "ANNEXES"
    }
    
    for zone_key, label in zone_labels.items():
        content = zones.get(zone_key, "").strip()
        if content:
            parts.append(f"=== {label} ===\n{content}")
    
    return "\n\n".join(parts)


def get_zone_summary(zones: dict, max_length: int = 500) -> str:
    """
    Get a summary of the decision zones.
    
    Args:
        zones: Dictionary with extracted zones
        max_length: Maximum length for each zone in summary
    
    Returns:
        Summary string
    """
    parts = []
    
    for zone_key in ["expose", "motivations", "dispositif"]:
        content = zones.get(zone_key, "").strip()
        if content:
            truncated = content[:max_length] + "..." if len(content) > max_length else content
            parts.append(f"**{zone_key.upper()}**: {truncated}")
    
    return "\n\n".join(parts) if parts else "Pas de zones disponibles."


def format_highlights(highlights: dict) -> str:
    """
    Format search highlights for display.
    
    Args:
        highlights: Dictionary with highlighted fragments
    
    Returns:
        Formatted string
    """
    parts = []
    
    for zone, fragments in highlights.items():
        if fragments:
            parts.append(f"=== {zone.upper()} ===")
            for fragment in fragments:
                # Convert <em> tags to markdown bold
                clean = fragment.replace("<em>", "**").replace("</em>", "**")
                parts.append(f"  • {clean}")
    
    return "\n".join(parts) if parts else "Pas de highlights disponibles."
