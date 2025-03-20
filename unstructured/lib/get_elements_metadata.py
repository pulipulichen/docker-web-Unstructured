import sys

def extract_metadata(element):
    metadata = {}
    try:
        
        # print('last_modified')
        if element.metadata.last_modified is not None:
            metadata["last_modified"] = element.metadata.last_modified
        
        # print('filetype')
        if element.metadata.filetype is not None:
            metadata["filetype"] = element.metadata.filetype

        # print('coordinates')
        if element.metadata.coordinates is not None:
            coordinates_dict = element.metadata.coordinates.to_dict()
            # print(coordinates_dict)
            if "points" in coordinates_dict:
                metadata["coordinates_top"] = round(coordinates_dict["points"][0][0], 2)
                metadata["coordinates_left"] = round(coordinates_dict["points"][0][1], 2)
                metadata["coordinates_bottom"] = round(coordinates_dict["points"][3][0], 2)
                metadata["coordinates_right"] = round(coordinates_dict["points"][3][1], 2)

        # print('parent_id')
        if element.metadata.parent_id is not None:
            metadata["parent_id"] = element.metadata.parent_id
            
        # print('category_depth')
        if element.metadata.category_depth is not None:
            metadata["category_depth"] = element.metadata.category_depth
        
        # print('emphasized_text_contents')
        if element.metadata.emphasized_text_contents is not None:
            metadata["emphasized_text_contents"] = element.metadata.emphasized_text_contents

        # print('emphasized_text_tags')
        if element.metadata.emphasized_text_tags is not None:
            metadata["emphasized_text_tags"] = element.metadata.emphasized_text_tags

        # print('is_continuation')
        if element.metadata.is_continuation is not None:
            metadata["is_continuation"] = vars(element.metadata.is_continuation)
    
        return metadata
    except Exception as e:
        print(f"Failed to extract metadata: {str(e)}")

    # print('extract_metadata', metadata)
    return metadata

def get_elements_metadata(first_element, last_element):
    first_element_metadata = extract_metadata(first_element)
    last_element_metadata = extract_metadata(last_element)

    output = {}
    for key in first_element_metadata.keys():
        output['start_' + key] = first_element_metadata[key]

    for key in last_element_metadata.keys():
        output['end_' + key] = last_element_metadata[key]

    return output


if __name__ == "__main__":
    get_elements_metadata(sys.argv[1])