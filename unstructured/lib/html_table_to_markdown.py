import sys

import re
from bs4 import BeautifulSoup
from html import unescape

def html_table_to_markdown(html_string):
    """
    Convert an HTML table with multiple row headers to a Markdown table.
    
    Args:
        html_string (str): HTML table as a string
        
    Returns:
        str: Markdown formatted table
    """
    # Parse the HTML
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    
    if not table:
        return "No table found in the provided HTML"
    
    # Extract header rows
    thead = table.find('thead')
    if not thead:
        return "No table header found in the provided HTML"
    
    header_rows = thead.find_all('tr')
    
    # Extract body rows
    tbody = table.find('tbody')
    if not tbody:
        return "No table body found in the provided HTML"
    
    body_rows = tbody.find_all('tr')
    
    # Determine the number of columns
    max_columns = 0
    for row in header_rows + body_rows:
        col_count = sum(int(cell.get('colspan', 1)) for cell in row.find_all(['th', 'td']))
        max_columns = max(max_columns, col_count)
    
    # Process header rows to create markdown header
    header_data = []
    
    for row in header_rows:
        row_data = []
        cells = row.find_all(['th', 'td'])
        
        for cell in cells:
            # Clean and normalize cell text
            text = cell.get_text().strip()
            text = re.sub(r'\s+', ' ', text)
            text = text.replace('\n', ' ')
            row_data.append(text)
        
        # Fill any missing columns
        while len(row_data) < max_columns:
            row_data.append("")
            
        header_data.append(row_data)
    
    # Combine multiple header rows if needed
    combined_header = []
    
    # Initialize combined header with first row
    for i in range(max_columns):
        if i < len(header_data[0]):
            combined_header.append(header_data[0][i])
        else:
            combined_header.append("")
    
    # Merge with subsequent header rows
    for row_idx in range(1, len(header_data)):
        for col_idx in range(len(header_data[row_idx])):
            if col_idx < max_columns:
                if header_data[row_idx][col_idx] and combined_header[col_idx]:
                    combined_header[col_idx] += " " + header_data[row_idx][col_idx]
                elif header_data[row_idx][col_idx]:
                    combined_header[col_idx] = header_data[row_idx][col_idx]
    
    # Generate markdown table
    markdown_lines = []
    
    # Add header
    markdown_lines.append("| " + " | ".join(combined_header) + " |")
    
    # Add separator line
    markdown_lines.append("| " + " | ".join(["---" for _ in range(max_columns)]) + " |")
    
    # Add body rows
    for row in body_rows:
        row_data = []
        cells = row.find_all(['th', 'td'])
        
        for cell in cells:
            # Clean and normalize cell text
            text = cell.get_text().strip()
            text = re.sub(r'\s+', ' ', text)
            text = text.replace('\n', ' ')
            row_data.append(text)
        
        # Fill any missing columns
        while len(row_data) < max_columns:
            row_data.append("")
            
        markdown_lines.append("| " + " | ".join(row_data) + " |")
    
    return "\n".join(markdown_lines)


if __name__ == "__main__":
    html_input = sys.argv[1]
    print(html_table_to_markdown(html_input))
