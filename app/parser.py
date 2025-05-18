import re
import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

def extract_name(text):
    # Simple heuristic: first non-empty line, assuming it’s the candidate’s name
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip():
            # Return first line with some reasonable length (to avoid junk)
            if len(line.strip()) < 50:
                return line.strip()
    return None

def extract_education(text):
    edu_keywords = ['education', 'degree', 'university', 'college', 'bachelor', 'master', 'phd', 'certification']
    lines = text.lower().split('\n')
    edu_lines = []
    capture = False
    for line in lines:
        if any(kw in line for kw in edu_keywords):
            capture = True
        if capture:
            edu_lines.append(line)
            # Stop after 5 lines or empty line (simple boundary)
            if len(edu_lines) > 5 or not line.strip():
                break
    return '\n'.join(edu_lines).strip() if edu_lines else None


def extract_email(text):
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    pattern = r'\+?\d[\d\s\-]{8,}\d'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_skills(text):
    skills_list = ['Python', 'JavaScript', 'React', 'SQL', 'Django', 'REST', 'Web Sockets']
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found_skills

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    name = extract_name(text)
    education = extract_education(text)
    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'education': education
    }

if __name__ == "__main__":
    resume_data = parse_resume('resumes/Resume.pdf')  # make sure this matches your file name
    print(resume_data)
