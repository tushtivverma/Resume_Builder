import fitz
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

def pdf_to_png(pdf_path, output_dir):
    # Open the PDF file
    pdf_file = fitz.open(pdf_path)
    
    # Iterate through each page of the PDF
    for page_num in range(len(pdf_file)):
        page = pdf_file.load_page(page_num)
        
        # Convert PDF page to image (PNG)
        image = page.get_pixmap()
        
        # Construct the output file path
        output_path = f"{output_dir}/page_{page_num + 1}.png"
        
        # Save the image
        image.save(output_path)
        
        print(f"Page {page_num + 1} saved as {output_path}")
    
    # Close the PDF file
    pdf_file.close()
    
    return output_path  # Return the last saved image path

def encode_image(image_path):
    """
    Encodes an image to base64 format.

    Args:
    image_path (str): The path to the image file.

    Returns:
    str: The base64 encoded string of the image content.
    """
    # Open the image file in binary-read mode and encode it to base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def summary_extract(img_url):
    system_prompt = '''
                    Your mission:

                    Extract the summary section from this image of a resume. Do not rewrite or make new sentences. 
                    '''

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_url}"},
                },
            ],
        },
    ],
        max_tokens=300,
        top_p=0.1
    )

    return response.choices[0].message.content

def work_exp_extract(img_url):
    system_prompt = '''
                    Your mission:

                    Extract the Work Experience section from this image of a resume. Do not rewrite or make new sentences. 
                    '''

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url":{"url":f"data:image/jpeg;base64,{img_url}"},
                },
            ],
        },
    ],
        max_tokens=300,
        top_p=0.1
    )

    return response.choices[0].message.content

def skill_extract(img_url):

    system_prompt = '''
                    Your mission:

                    Extract the Skills section from this image of a resume. Do not rewrite or make new sentences. 
                    '''

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url":{"url":f"data:image/jpeg;base64,{img_url}"},
                },
            ],
        },
    ],
        max_tokens=500,
        top_p=0.1
    )

    return response.choices[0].message.content

def extract_miscellaneous(img_url):

    system_prompt = '''
                    Your mission:

                    Go through the whole document provided.
                    Extract everything else except the Summary, Work Experinece, and the Skills section from this image of a resume. 
                    Do not rewrite or make new sentences. 
                    Make sure you add every sentence mentioned in those sections
                    '''

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url":f"data:image/jpeg;base64,{img_url}"},
                },
            ],
        },
    ],
        max_tokens=1000,
        top_p=0.1
    )

    return response.choices[0].message.content

def main(pdf_path, output_dir):

    # Convert the PDF page to an image
    output_image_path = pdf_to_png(pdf_path, output_dir)
    print(output_image_path)

    # base64 encode
    encode = encode_image(output_image_path)

    # Extract the Summary section from the document
    summary = summary_extract(encode)

    # Extract the Work Experience section from the document
    work_exp = work_exp_extract(encode)

    # Extract the Skill section from the document
    skill = skill_extract(encode)

    # Extract everything else
    misc = extract_miscellaneous(encode)

    resume = {'summary' :summary, 'wexp': work_exp, 'skill': skill, 'miscellaneous': misc}

    print(resume["summary"])

if __name__ == "__main__":
    main(pdf_path='resumepdf/TushtiVVermaResume.pdf', output_dir="temp_img")
