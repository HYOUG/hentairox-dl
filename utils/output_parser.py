from xml.sax.handler import property_dom_node

from pathvalidate import sanitize_filename, sanitize_filepath


def parse_output(output_path:str, properties:dict) -> str:
    clean_properties = properties.copy()
    clean_path = output_path
    
    for (key, value) in clean_properties.items():
        clean_properties[key] = sanitize_filename(str(value), replacement_text="-")
        
    clean_path = clean_path.format(**clean_properties)
    clean_path = sanitize_filepath(clean_path, replacement_text="-")
    clean_path = " ".join(clean_path.split())
    
    return clean_path