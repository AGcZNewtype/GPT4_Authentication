import PyPDF2

# Extract text from a PDF file
def extract_text_from_pdf(file_path):
    pdf_text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Split and merge GPT output questions and answers
def response_split(response):
    # Split questions and answers by the '==' delimiter
    allList = response.split('==')
    quesList = []
    ansList = []

    for i in allList:
        if i.find("++") != -1:
            templist = i.split("++")
            # Add to question list
            quesList.append(templist[0])
            # Add to answer list
            ansList.append(templist[1])

    # print(quesList)
    # print(ansList)
    return quesList, ansList

# Calculate the average similarity
def avg_similarity(similarity):
    totalSimilarity = float()
    for i in similarity:
        totalSimilarity += float(i)
    average = totalSimilarity / (len(similarity))
    print(average)
    return average

