import os
import base64
from openai import OpenAI
from pathlib import Path
from prompt.general import prompt

def process_pdf_to_text(pdf_path):
    client = OpenAI()
    
    # Read the PDF file
    with open(pdf_path, "rb") as f:
        data = f.read()
    
    # Convert to base64
    base64_string = base64.b64encode(data).decode("utf-8")
    
    # Get the content using OpenAI API
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": pdf_path.name,
                        "file_data": f"data:application/pdf;base64,{base64_string}",
                    },
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                ],
            },
        ]
    )
    
    return response.output_text

def main():
    # Base path for PEC folders
    base_path = Path("brasil/2025/pec")
    
    # Iterate through all PEC folders
    for pec_folder in base_path.glob("pec-*"):
        print(f"Processing folder: {pec_folder}")
        
        # Find all PDF files in the folder
        for pdf_file in pec_folder.glob("*.pdf"):
            # Generate the corresponding txt filename
            txt_file = pdf_file.with_suffix(".txt")
            
            # Check if txt file already exists
            if txt_file.exists():
                print(f"Skipping {pdf_file.name} - text file already exists")
                continue
            
            print(f"Processing {pdf_file.name}")
            try:
                # Process the PDF and get the text
                text_content = process_pdf_to_text(pdf_file)
                
                # Write the text to a file
                with open(txt_file, "w", encoding="utf-8") as f:
                    f.write(text_content)
                
                print(f"Successfully created {txt_file.name}")
                
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}")

if __name__ == "__main__":
    main() 