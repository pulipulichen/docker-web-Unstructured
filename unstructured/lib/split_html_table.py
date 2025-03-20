import sys
from bs4 import BeautifulSoup

def split_html_table(html: str, rows_per_table: int = 50) -> list:
    """
    Splits an HTML table into multiple tables, each containing a fixed number of rows.
    
    Parameters:
        html (str): The original HTML table as a string.
        rows_per_table (int, optional): Number of rows per split table. Default is 50.
    
    Returns:
        list: A list of HTML strings, each representing a split table.
    """
    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract table elements
    original_table = soup.find("table")
    if not original_table:
        return []
    
    thead = original_table.find("thead")
    tbody = original_table.find("tbody")
    tfoot = original_table.find("tfoot")

    # Extract all rows, checking if <tbody> exists
    if not tbody:
        rows = original_table.find_all("tr")
    else:
        rows = tbody.find_all("tr")

    # If no <thead>, use the first row as the new thead
    if (not thead or not thead.find_all("tr")) and rows:
        thead = soup.new_tag("thead")
        first_row = rows.pop(0)
        thead.append(first_row)

        # If the first row has an empty first column, keep adding rows until a non-empty first column is found
        # while rows and not first_row.find_all("td")[0].get_text(strip=True):
        #     first_row = rows.pop(0)
        #     thead.append(first_row)

        # # If the first column of a row is empty, move the row to thead
        # while rows and rows[0].find_all("td")[0].get_text(strip=True):
        #     first_row = rows.pop(0)
        #     thead.append(first_row)

        # If the next row has a value in the first column but the row after that does not, add both rows to thead
        # print(rows[0].find_all("td")[0].get_text(strip=True))
        # print(rows[1].find_all("td")[0].get_text(strip=True))
        while len(rows) > 1 and rows[0].find_all("td")[0].get_text(strip=True) and not rows[1].find_all("td")[0].get_text(strip=True):
            thead.append(rows.pop(0))
            thead.append(rows.pop(0))
 
    for cell in thead.find_all("td"):
        cell.name = "th"  # Convert <td> to <th>

    # Split rows into chunks of given size
    chunks = [rows[i:i + rows_per_table] for i in range(0, len(rows), rows_per_table)]

    # Generate new tables
    split_tables = []
    for chunk in chunks:
        new_table = BeautifulSoup("<table></table>", "html.parser").table
        if thead:
            new_table.append(thead)
        
        new_tbody = soup.new_tag("tbody")
        for row in chunk:
            new_tbody.append(row)
        new_table.append(new_tbody)

        # Append <tfoot> if it exists
        if tfoot:
            new_table.append(tfoot)

        split_tables.append(str(new_table))

    return split_tables


if __name__ == "__main__":
    split_html_table(sys.argv[1])
